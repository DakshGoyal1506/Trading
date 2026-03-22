from __future__ import annotations

from datetime import date, datetime

import pandas as pd
import yfinance as yf

from src.data.providers.base import HistoricalDataProvider


class YahooFinanceProvider(HistoricalDataProvider):
    def __init__(self, auto_adjust: bool = False) -> None:
        self.auto_adjust = auto_adjust

    def provider_name(self) -> str:
        return "yahoo"

    def get_daily_bars(self, instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame:
        df = yf.download(
            instrument_id,
            start=datetime.combine(start_date, datetime.min.time()).isoformat(),
            end=datetime.combine(end_date, datetime.min.time()).isoformat(),
            interval="1d",
            auto_adjust=self.auto_adjust,
            progress=False,
        )

        empty_cols = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
            "symbol",
            "data_source",
        ]

        if df is None or df.empty:
            return pd.DataFrame(columns=empty_cols)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        rename_map = {
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        }
        df = df.rename(columns=rename_map)

        df = df.reset_index().rename(columns={"Date": "timestamp"})
        if "adj_close" not in df.columns:
            df["adj_close"] = pd.NA

        df["symbol"] = instrument_id
        df["data_source"] = self.provider_name()

        return df[empty_cols]

    def get_instruments(self) -> pd.DataFrame:
        return pd.DataFrame(columns=["symbol", "exchange", "instrument_id", "data_source"])

    def get_corporate_actions(self, instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame:
        ticker = yf.Ticker(instrument_id)

        start_dt = datetime.combine(start_date, datetime.min.time())
        end_dt = datetime.combine(end_date, datetime.min.time())

        dividends = ticker.dividends[start_dt:end_dt].reset_index()
        dividends["action_type"] = "dividend"
        dividends["value"] = dividends["Dividends"]
        dividends = dividends.drop(columns=["Dividends"])

        splits = ticker.splits[start_dt:end_dt].reset_index()
        splits["action_type"] = "split"
        splits["value"] = splits["Stock Splits"]
        splits = splits.drop(columns=["Stock Splits"])

        corporate_actions = pd.concat([dividends, splits], ignore_index=True)
        if corporate_actions.empty:
            return pd.DataFrame(columns=["instrument_id", "ex_date", "action_type", "value", "data_source"])

        corporate_actions = corporate_actions.rename(columns={"Date": "ex_date"})
        corporate_actions["instrument_id"] = instrument_id
        corporate_actions["data_source"] = self.provider_name()

        return corporate_actions[["instrument_id", "ex_date", "action_type", "value", "data_source"]]