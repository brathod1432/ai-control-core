from functools import lru_cache

from app.config import get_settings
from app.providers.base import MarketDataProvider
from app.providers.sample import SampleMarketDataProvider


@lru_cache
def get_market_data_provider() -> MarketDataProvider:
    settings = get_settings()
    if settings.data_provider == "sample":
        return SampleMarketDataProvider()
    raise ValueError(f"Unsupported market data provider: {settings.data_provider}")

