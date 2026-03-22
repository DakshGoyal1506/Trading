from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional, Union, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class Instrument(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    symbol: str = Field(..., description="Trading symbol of the instrument", min_length=1)
    exchange: str = Field(..., description="Exchange where the instrument is traded", min_length=1)
    asset_class: Literal["equity", "eft", "index", "option", "future", "currency", "commodity", "crypto"] = Field(default="equity", description="Asset class of the instrument")
    currency: str = Field(default="INR", description="Currency of the instrument")
    tick_size: float = Field(default=0.05, description="Minimum price movement of the instrument", gt=0)
    lot_size: int = Field(default=1, description="Minimum trading quantity of the instrument", gt=1)
    is_active: bool = Field(default=True, description="Whether the instrument is currently active for trading")

    @field_validator("currency", "exchange", mode="before")
    @classmethod
    def uppercase_text(cls, value: str) -> str:
        return value.upper() if isinstance(value, str) else value
    
class Bar(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    timestamp: datetime = Field(..., description="Timestamp of the bar")
    open: float = Field(..., description="Opening price of the bar", gt=0)
    high: float = Field(..., description="Highest price of the bar", gt=0)
    low: float = Field(..., description="Lowest price of the bar", gt=0)
    close: float = Field(..., description="Closing price of the bar", gt=0)
    volume: int = Field(default=0, description="Trading volume during the bar", ge=0)
    adj_close: Optional[float] = Field(default=None, description="Adjusted closing price of the bar")
    data_source: Literal["yahoo", "zerodha"]

    @model_validator(mode="after")
    def validate_ohlc(self) -> "Bar":
        if self.high < self.low:
            raise ValueError("High price cannot be less than low price")
        if not (self.low <= self.open <= self.high):
            raise ValueError("Open price must be between low and high price")
        if not (self.low <= self.close <= self.high):
            raise ValueError("Close price must be between low and high price")
        if self.adj_close is not None and self.adj_close <= 0:
            raise ValueError("Adjusted close price must be greater than 0") 
        return self

class CorporateAction(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    action_type: Literal["dividend", "split", "bonus", "merger", "demerger"] = Field(..., description="Type of corporate action")
    ex_date: date = Field(..., description="Date of the corporate action")
    value: Optional[Union[float, str]] = Field(default=None, description="Value associated with the corporate action (e.g., dividend amount, split ratio)")
    notes: Optional[str] = Field(default=None, description="Additional details about the corporate action")

class DatasetMetadata(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    dataset_name: str = Field(..., description="Name of the dataset", min_length=1)
    source: Literal["yahoo", "zerodha"] = Field(..., description="Source of the dataset")
    universe: str = Field(..., description="Universe of the dataset", min_length=1)
    timeframe: str = Field(..., description="Timeframe of the dataset", min_length=1)
    start_date: date
    end_date: date
    created_at: datetime
    version: str = Field(..., description="Version of the dataset", min_length=1)

    @model_validator(mode="after")
    def validate_dates(self) -> "DatasetMetadata":
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        return self