from __future__ import annotations

from statistics import mean

from app.domain import IndicatorSnapshot, MarketBar


def simple_moving_average(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return round(mean(values[-period:]), 4)


def exponential_moving_average(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)
    ema = mean(values[:period])
    for value in values[period:]:
        ema = (value - ema) * multiplier + ema
    return round(ema, 4)


def relative_strength_index(values: list[float], period: int = 14) -> float | None:
    if len(values) <= period:
        return None

    gains: list[float] = []
    losses: list[float] = []

    for previous, current in zip(values[-period - 1 : -1], values[-period:]):
        change = current - previous
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))

    average_gain = mean(gains)
    average_loss = mean(losses)
    if average_loss == 0:
        return 100.0

    relative_strength = average_gain / average_loss
    return round(100 - (100 / (1 + relative_strength)), 2)


def average_true_range(bars: list[MarketBar], period: int = 14) -> float | None:
    if len(bars) <= period:
        return None

    true_ranges = []
    recent = bars[-period:]
    previous_close = bars[-period - 1].close
    for bar in recent:
        true_ranges.append(
            max(
                bar.high - bar.low,
                abs(bar.high - previous_close),
                abs(bar.low - previous_close),
            )
        )
        previous_close = bar.close

    return round(mean(true_ranges), 4)


def volume_ratio(bars: list[MarketBar], period: int = 20) -> float | None:
    if len(bars) <= period:
        return None

    average_volume = mean(bar.volume for bar in bars[-period - 1 : -1])
    if average_volume == 0:
        return None
    return round(bars[-1].volume / average_volume, 3)


def build_indicator_snapshot(bars: list[MarketBar]) -> IndicatorSnapshot:
    closes = [bar.close for bar in bars]
    return IndicatorSnapshot(
        sma_20=simple_moving_average(closes, 20),
        sma_50=simple_moving_average(closes, 50),
        ema_12=exponential_moving_average(closes, 12),
        ema_26=exponential_moving_average(closes, 26),
        rsi_14=relative_strength_index(closes, 14),
        atr_14=average_true_range(bars, 14),
        volume_ratio=volume_ratio(bars, 20),
    )

