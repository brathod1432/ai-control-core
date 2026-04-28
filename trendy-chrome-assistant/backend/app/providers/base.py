from abc import ABC, abstractmethod

from app.domain import MarketBar
from app.models import Timeframe


class MarketDataProvider(ABC):
    name: str

    @abstractmethod
    def fetch(self, symbol: str, timeframe: Timeframe, lookback: int) -> list[MarketBar]:
        """Fetch historical market bars."""

