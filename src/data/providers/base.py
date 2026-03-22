from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

import pandas as pd


class HistoricalDataProvider(ABC):
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError("Subclasses must implement provider_name method")

    @abstractmethod
    def get_daily_bars(self, instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame:
        """Return daily OHLCV bars in canonical columns."""
        raise NotImplementedError("Subclasses must implement get_daily_bars method")

    @abstractmethod
    def get_instruments(self) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement get_instruments method")

    @abstractmethod
    def get_corporate_actions(
        self, instrument_id: str, start_date: date, end_date: date
    ) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement get_corporate_actions method")