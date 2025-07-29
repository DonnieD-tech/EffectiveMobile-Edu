from sqlalchemy import select, distinct, desc, and_, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trading_result import SpimexTradingResult
from app.schemas.filters import DynamicsFilter, TradingResultFilter


async def get_last_trading_dates(db: AsyncSession, limit: int = 5) -> list:
    base_request = (
        select(distinct(SpimexTradingResult.date))
        .order_by(desc(SpimexTradingResult.date))
        .limit(limit)
    )
    result = await db.execute(base_request)
    return [row[0] for row in result.fetchall()]


async def get_dynamics(db: AsyncSession, filters: DynamicsFilter) -> Sequence[SpimexTradingResult]:
    conditions = [
        SpimexTradingResult.date >= filters.start_date,
        SpimexTradingResult.date <= filters.end_date
    ]

    if filters.oil_id:
        conditions.append(SpimexTradingResult.oil_id == filters.oil_id)

    if filters.delivery_type_id:
        conditions.append(SpimexTradingResult.delivery_type_id == filters.delivery_type_id)

    if filters.delivery_basis_id:
        conditions.append(SpimexTradingResult.delivery_basis_id == filters.delivery_basis_id)

    base_request = select(SpimexTradingResult).where(and_(*conditions)).order_by(SpimexTradingResult.date)
    result = await db.execute(base_request)
    return result.scalars().all()


async def get_trading_results(db: AsyncSession, filters: TradingResultFilter) -> Sequence[SpimexTradingResult]:
    conditions = [SpimexTradingResult.oil_id == filters.oil_id]

    if filters.delivery_type_id:
        conditions.append(SpimexTradingResult.delivery_type_id == filters.delivery_type_id)

    if filters.delivery_basis_id:
        conditions.append(SpimexTradingResult.delivery_basis_id == filters.delivery_basis_id)

    base_request = (
        select(SpimexTradingResult)
        .where(and_(*conditions))
        .order_by(SpimexTradingResult.date.desc())
        .limit(filters.limit)
    )

    result = await db.execute(base_request)
    return result.scalars().all()
