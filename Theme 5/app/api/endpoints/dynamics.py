from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.trading_result import TradingResultOut
from app.schemas.filters import DynamicsFilter
from app.crud.trading_results import get_dynamics
from app.services.cache import make_cache_key, get_or_set_cache
from typing import List

router = APIRouter()

@router.get("/dynamics", response_model=List[TradingResultOut])
async def dynamics(
    start_date: str = Query(...),
    end_date: str = Query(...),
    oil_id: str = Query(None),
    delivery_type_id: str = Query(None),
    delivery_basis_id: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    filters = DynamicsFilter(
        start_date=start_date,
        end_date=end_date,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id
    )

    key = make_cache_key("dynamics", filters.model_dump())

    async def get_data():
        result = await get_dynamics(db, filters)
        return [TradingResultOut.model_validate(row).model_dump() for row in result]

    return await get_or_set_cache(key, get_data)

