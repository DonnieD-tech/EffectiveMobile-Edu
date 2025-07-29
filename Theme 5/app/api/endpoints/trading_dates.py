from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.trading_results import get_last_trading_dates
from app.services.cache import make_cache_key, get_or_set_cache
from typing import List
from datetime import date

router = APIRouter()

@router.get("/last-trading-dates", response_model=List[date])
async def last_trading_dates(
    limit: int = Query(5, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    key = make_cache_key("last-trading-dates", {"limit": limit})

    async def get_data():
        result = await get_last_trading_dates(db, limit)
        return [d.isoformat() for d in result]

    return await get_or_set_cache(key, get_data)

