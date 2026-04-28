from __future__ import annotations

from datetime import UTC, datetime, timedelta
from random import Random

from app.domain import MarketBar, MarketDataError
from app.models import Timeframe
from app.providers.base import MarketDataProvider


class SampleMarketDataProvider(MarketDataProvider):
    """Deterministic local market data for development and demos."""

    name = "sample"

    def fetch(self, symbol: str, timeframe: Timeframe, lookback: int) -> list[MarketBar]:
        normalized_symbol = symbol.strip().upper()
        if not normalized_symbol:
            raise MarketDataError("Symbol is required.")

        seed = sum(ord(char) for char in f"{normalized_symbol}:{timeframe}:{lookback}")
        random = Random(seed)
        interval = _interval_for(timeframe)
        now = datetime.now(UTC).replace(microsecond=0)

        base_price = 30 + random.random() * 220
        phase_shift = random.uniform(-0.9, 0.9)
        price = base_price
        bars: list[MarketBar] = []

        for index in range(lookback):
            regime = _market_regime(index, lookback, phase_shift)
            move = random.uniform(-1.9, 2.0) + regime
            open_price = price
            close_price = max(1.0, price + move)
            high_price = max(open_price, close_price) + random.uniform(0.08, 1.5)
            low_price = max(0.5, min(open_price, close_price) - random.uniform(0.08, 1.5))
            volume = int(650_000 + random.random() * 4_000_000)

            bars.append(
                MarketBar(
                    timestamp=now - interval * (lookback - index - 1),
                    open=round(open_price, 2),
                    high=round(high_price, 2),
                    low=round(low_price, 2),
                    close=round(close_price, 2),
                    volume=volume,
                )
            )
            price = close_price

        return bars


def _interval_for(timeframe: Timeframe) -> timedelta:
    return {
        "1d": timedelta(days=1),
        "1wk": timedelta(weeks=1),
        "1mo": timedelta(days=30),
    }[timeframe]


def _market_regime(index: int, lookback: int, phase_shift: float) -> float:
    progress = index / max(lookback - 1, 1)
    if progress < 0.35:
        return -0.05 + phase_shift * 0.08
    if progress < 0.7:
        return 0.03
    return 0.11 + phase_shift * 0.04

