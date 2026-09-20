from __future__ import annotations

from datetime import datetime
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Timeframe = Literal["1d", "1wk", "1mo"]
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9.\-^=]+$")


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str
    provider: str


class AppConfigResponse(BaseModel):
    app_name: str
    app_version: str
    data_provider: str
    supported_timeframes: list[str]


class AnalysisRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=16, pattern=r"^[A-Za-z0-9.\-^=]+$")
    timeframe: Timeframe = "1d"
    lookback: int = Field(default=90, ge=60, le=240)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.strip().upper()


class BatchAnalysisRequest(BaseModel):
    symbols: list[str] = Field(min_length=1, max_length=12)
    timeframe: Timeframe = "1d"
    lookback: int = Field(default=90, ge=60, le=240)

    @field_validator("symbols")
    @classmethod
    def normalize_symbols(cls, values: list[str]) -> list[str]:
        normalized = []
        for value in values:
            symbol = value.strip().upper()
            if symbol and not SYMBOL_PATTERN.match(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            if symbol and symbol not in normalized:
                normalized.append(symbol)
        return normalized


class PricePoint(BaseModel):
    timestamp: datetime
    close: float


class IndicatorResponse(BaseModel):
    sma_20: float | None
    sma_50: float | None
    ema_12: float | None
    ema_26: float | None
    rsi_14: float | None
    atr_14: float | None
    volume_ratio: float | None


class AnalysisResponse(BaseModel):
    symbol: str
    timeframe: Timeframe
    provider: str
    last_close: float
    change_percent: float
    signal: str
    trend: str
    momentum: str
    confidence: int = Field(ge=0, le=100)
    indicators: IndicatorResponse
    summary: str
    risk_note: str
    price_points: list[PricePoint]


class BatchAnalysisResponse(BaseModel):
    results: list[AnalysisResponse]
