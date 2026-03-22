from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional, Union, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

class Signal(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    signal_id: str = Field(..., description="Unique identifier for the signal", min_length=1)
    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    timestamp: datetime = Field(..., description="Timestamp of the signal")
    stratergy_name: str = Field(..., description="Name of the strategy that generated the signal", min_length=1)
    direction: Literal["LONG", "SHORT", "FLAT"] = Field(..., description="Side of the signal")
    score: Optional[float] = Field(default=None, description="Confidence level of the signal (0 to 1)")
    notes: Optional[str] = Field(default=None, description="Additional details about the signal")

class TargetPosition(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    target_quantity: int = Field(..., description="Target quantity for the position", ge=0)
    target_price: Optional[float] = Field(default=None, description="Target price for the position", gt=0)
    timestamp: datetime = Field(..., description="Timestamp of the target position")
    stratergy_name: str = Field(..., description="Name of the strategy that generated the signal", min_length=1)

class BacktestRun(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    run_id: str = Field(..., description="Unique identifier for the backtest run", min_length=1)
    strategy_name: str = Field(..., description="Name of the strategy being backtested", min_length=1)
    config_path: str = Field(..., description="Path to the configuration file used for the backtest", min_length=1)
    universe_name: str = Field(..., description="Name of the universe used for the backtest", min_length=1)
    start_date: date = Field(..., description="Start date of the backtest")
    end_date: date = Field(..., description="End date of the backtest")
    cost_model_name: str = Field(..., description="Name of the cost model used for the backtest", min_length=1)
    initial_capital: float = Field(..., description="Initial capital for the backtest", gt=0)
    final_capital: Optional[float] = Field(default=None, description="Final capital at the end of the backtest", gt=0)
    total_return: Optional[float] = Field(default=None, description="Total return of the strategy over the backtest period")
    annualized_return: Optional[float] = Field(default=None, description="Annualized return of the strategy over the backtest period")
    max_drawdown: Optional[float] = Field(default=None, description="Maximum drawdown during the backtest period")
    notes: Optional[str] = Field(default=None, description="Additional details about the backtest run")

    @model_validator(mode="after")
    def validate_dates(self) -> "BacktestRun":
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be earlier than start_date")
        return self