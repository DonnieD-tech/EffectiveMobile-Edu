from pydantic import BaseModel
from typing import Optional
from datetime import date


class DynamicsFilter(BaseModel):
    start_date: date
    end_date: date
    oil_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None


class TradingResultFilter(BaseModel):
    oil_id: str
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None
    limit: Optional[int] = 10
