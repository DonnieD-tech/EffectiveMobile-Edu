from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.trading_result import TradingResultOut
from app.schemas.filters import TradingResultFilter
from app.crud.trading_results import get_trading_results
from app.core.database import get_db
from app.services.cache import make_cache_key, get_or_set_cache

router = APIRouter()

@router.get("/trading-results", response_model=List[TradingResultOut])
async def trading_results(
    oil_id: str = Query(...),
    delivery_type_id: str = Query(None),
    delivery_basis_id: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    filters = TradingResultFilter(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
        limit=limit
    )

    key = make_cache_key("trading-results", filters.model_dump())

    async def get_data():
        result = await get_trading_results(db, filters)
        return [TradingResultOut.model_validate(row).model_dump() for row in result]

    return await get_or_set_cache(key, get_data)
