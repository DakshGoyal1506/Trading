from __future__ import annotations

import hashlib
from datetime import date
from io import StringIO
from typing import Optional

import pandas as pd
import requests

from src.data.providers.base import HistoricalDataProvider


class ZerodhaProvider(HistoricalDataProvider):
    BASE_URL = "https://api.kite.trade"
    LOGIN_URL = "https://kite.zerodha.com/connect/login"

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        access_token: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.timeout = timeout

    def provider_name(self) -> str:
        return "zerodha"

    def get_login_url(self) -> str:
        return f"{self.LOGIN_URL}?v=3&api_key={self.api_key}"

    def generate_session(self, request_token: str) -> dict:
        checksum = hashlib.sha256(
            f"{self.api_key}{request_token}{self.api_secret}".encode("utf-8")
        ).hexdigest()

        response = requests.post(
            f"{self.BASE_URL}/session/token",
            headers={"X-Kite-Version": "3"},
            data={
                "api_key": self.api_key,
                "request_token": request_token,
                "checksum": checksum,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        self.access_token = payload["data"]["access_token"]
        return payload["data"]

    def _headers(self) -> dict:
        if not self.access_token:
            raise ValueError("access_token is missing")
        return {
            "X-Kite-Version": "3",
            "Authorization": f"token {self.api_key}:{self.access_token}",
        }

    def get_instruments(self) -> pd.DataFrame:
        response = requests.get(
            f"{self.BASE_URL}/instruments",
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))
        if "instrument_token" in df.columns:
            df["instrument_id"] = df["instrument_token"].astype(str)
        else:
            df["instrument_id"] = pd.NA

        df["data_source"] = self.provider_name()
        return df

    def get_daily_bars(self, instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame:
        # Here instrument_id is treated as a trading symbol (e.g., "INFY").
        symbol = instrument_id

        instruments = self.get_instruments()
        row = instruments[
            (instruments["tradingsymbol"] == symbol) & (instruments["exchange"] == "NSE")
        ]

        if row.empty:
            raise ValueError(f"instrument token not found for symbol={symbol}")

        instrument_token = str(row.iloc[0]["instrument_token"])

        params = {
            "from": f"{start_date.isoformat()} 00:00:00",
            "to": f"{end_date.isoformat()} 23:59:59",
            "continuous": 0,
            "oi": 0,
        }

        response = requests.get(
            f"{self.BASE_URL}/instruments/historical/{instrument_token}/day",
            headers=self._headers(),
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()

        payload = response.json()
        candles = payload.get("data", {}).get("candles", [])

        rows: list[dict] = []
        for candle in candles:
            rows.append(
                {
                    "timestamp": pd.to_datetime(candle[0]),
                    "open": candle[1],
                    "high": candle[2],
                    "low": candle[3],
                    "close": candle[4],
                    "adj_close": pd.NA,
                    "volume": candle[5],
                    "symbol": symbol,
                    "data_source": self.provider_name(),
                }
            )

        return pd.DataFrame(rows)

    def get_corporate_actions(self, instrument_id: str, start_date: date, end_date: date) -> pd.DataFrame:
        # Zerodha corporate actions endpoint not wired yet.
        return pd.DataFrame(columns=["instrument_id", "ex_date", "action_type", "value", "data_source"])