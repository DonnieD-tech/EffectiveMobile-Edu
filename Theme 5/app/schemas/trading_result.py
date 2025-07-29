from pydantic import BaseModel
from datetime import date

class TradingResultOut(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: float
    total: float
    count: int
    date: date

    model_config = {
        "from_attributes": True
    }
