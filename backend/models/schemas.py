from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class StockPrice(BaseModel):
    symbol: str
    price: float
    previous_close: float
    change: float
    change_percent: float
    updated_at: datetime


class AlertCreate(BaseModel):
    symbol: str
    condition: Literal["above", "below"]
    target_price: float = Field(gt=0)


class Alert(BaseModel):
    id: str
    symbol: str
    condition: Literal["above", "below"]
    target_price: float
    triggered: bool = False
    created_at: datetime
    triggered_at: Optional[datetime] = None


class TriggeredAlert(BaseModel):
    id: str
    symbol: str
    condition: Literal["above", "below"]
    target_price: float
    current_price: float
    triggered_at: datetime


class PriceUpdateMessage(BaseModel):
    type: Literal["price_update"] = "price_update"
    stocks: List[StockPrice]
    triggered_alerts: List[TriggeredAlert] = []
