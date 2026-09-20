from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketBar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class IndicatorSnapshot:
    sma_20: float | None
    sma_50: float | None
    ema_12: float | None
    ema_26: float | None
    rsi_14: float | None
    atr_14: float | None
    volume_ratio: float | None


class MarketDataError(RuntimeError):
    """Raised when market data cannot be fetched."""

