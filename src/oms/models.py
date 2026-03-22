from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

class Order(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    order_id: str = Field(..., description="Unique identifier for the order", min_length=1)
    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    quantity: int = Field(..., description="Quantity of the order", ge=1)
    limit_price: Optional[float] = Field(default=None, description="Limit price (required for LIMIT)", gt=0)
    side: Literal["BUY", "SELL"] = Field(..., description="Side of the order")
    order_type: Literal["MARKET", "LIMIT", "SL", "SL-M"] = Field(..., description="Type of the order")
    timestamp: datetime = Field(..., description="Timestamp of the order")
    status: Literal["PENDING", "FILLED", "CANCELLED", "REJECTED", "EXPIRED", "OPEN"] = Field(
        default="PENDING", description="Status of the order"
    )
    exchange_order_id: Optional[str] = Field(
        default=None, description="Unique identifier for the order assigned by the exchange"
    )

    @model_validator(mode="after")
    def validate_limit_order(self) -> "Order":
        if self.order_type == "LIMIT":
            if self.limit_price is None:
                raise ValueError("limit_price must be provided for LIMIT orders")
            if self.limit_price <= 0:
                raise ValueError("limit_price must be greater than 0 for LIMIT orders")
        return self

class Fill(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    fill_id: str = Field(..., description="Unique identifier for the fill", min_length=1)
    order_id: str = Field(..., description="Unique identifier for the order associated with the fill", min_length=1)
    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    quantity: int = Field(..., description="Quantity filled", ge=1)
    price: float = Field(..., description="Price at which the order was filled", gt=0)
    timestamp: datetime = Field(..., description="Timestamp of the fill")
    fees: float = Field(default=0, description="Fee associated with the fill", ge=0)
    slippage_bps: float = Field(default=0, description="Slippage in basis points", ge=0)

class Position(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    instrument_id: str = Field(..., description="Unique identifier for the instrument", min_length=1)
    quantity: int = Field(..., description="Quantity of the position")
    average_price: float = Field(..., description="Average price of the position", gt=0)
    market_value: float = Field(default=0, description="Current market value of the position")
    unrealized_pnl: float = Field(default=0, description="Unrealized profit and loss of the position")