from __future__ import annotations

from app.domain import IndicatorSnapshot, MarketBar
from app.models import AnalysisRequest, AnalysisResponse, IndicatorResponse, PricePoint
from app.services.indicators import build_indicator_snapshot


def analyze_market_data(request: AnalysisRequest, bars: list[MarketBar], provider: str) -> AnalysisResponse:
    indicators = build_indicator_snapshot(bars)
    last_close = bars[-1].close
    previous_close = bars[-2].close
    change_percent = ((last_close - previous_close) / previous_close) * 100 if previous_close else 0
    trend = _derive_trend(last_close, indicators)
    momentum = _derive_momentum(indicators)
    signal = _derive_signal(trend, momentum, change_percent)
    confidence = _derive_confidence(trend, momentum, indicators)

    return AnalysisResponse(
        symbol=request.symbol,
        timeframe=request.timeframe,
        provider=provider,
        last_close=round(last_close, 2),
        change_percent=round(change_percent, 2),
        signal=signal,
        trend=trend,
        momentum=momentum,
        confidence=confidence,
        indicators=IndicatorResponse(**indicators.__dict__),
        summary=_build_summary(request.symbol, last_close, indicators, trend, momentum),
        risk_note=(
            "Educational analysis only. This does not place trades or replace "
            "independent research, position sizing, and risk management."
        ),
        price_points=[
            PricePoint(timestamp=bar.timestamp, close=bar.close)
            for bar in bars[-40:]
        ],
    )


def _derive_trend(last_close: float, indicators: IndicatorSnapshot) -> str:
    if indicators.sma_20 is None or indicators.sma_50 is None:
        return "Insufficient data"
    if indicators.sma_20 > indicators.sma_50 and last_close > indicators.sma_20:
        return "Uptrend"
    if indicators.sma_20 < indicators.sma_50 and last_close < indicators.sma_20:
        return "Downtrend"
    return "Sideways"


def _derive_momentum(indicators: IndicatorSnapshot) -> str:
    rsi = indicators.rsi_14
    if rsi is None:
        return "Unknown"
    if rsi >= 70:
        return "Overbought"
    if rsi >= 58:
        return "Strong"
    if rsi <= 30:
        return "Oversold"
    if rsi <= 42:
        return "Weak"
    return "Neutral"


def _derive_signal(trend: str, momentum: str, change_percent: float) -> str:
    if trend == "Uptrend" and momentum in {"Strong", "Neutral"} and change_percent >= -1:
        return "Watch bullish continuation"
    if trend == "Downtrend" and momentum in {"Weak", "Neutral"} and change_percent <= 1:
        return "Watch downside risk"
    if momentum in {"Overbought", "Oversold"}:
        return "Wait for confirmation"
    return "Hold / wait"


def _derive_confidence(trend: str, momentum: str, indicators: IndicatorSnapshot) -> int:
    score = 35
    if trend in {"Uptrend", "Downtrend"}:
        score += 20
    if momentum in {"Strong", "Weak", "Neutral"}:
        score += 15
    if indicators.volume_ratio is not None and indicators.volume_ratio >= 1:
        score += 10
    if indicators.atr_14 is not None:
        score += 10
    if indicators.rsi_14 is not None:
        score += 10
    return min(score, 100)


def _build_summary(symbol: str, last_close: float, indicators: IndicatorSnapshot, trend: str, momentum: str) -> str:
    sma_text = "moving averages are still warming up"
    if indicators.sma_20 is not None and indicators.sma_50 is not None:
        sma_text = f"20 SMA {indicators.sma_20:.2f} vs 50 SMA {indicators.sma_50:.2f}"

    rsi_text = "RSI unavailable"
    if indicators.rsi_14 is not None:
        rsi_text = f"RSI {indicators.rsi_14:.1f}"

    return f"{symbol} closed at {last_close:.2f}. Trend reads {trend}; momentum reads {momentum}; {sma_text}; {rsi_text}."

