from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.redis_cache import init_redis
from app.api.endpoints import trading_dates, dynamics, trading_results



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    print("✅ Redis подключен")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(trading_dates.router)
app.include_router(dynamics.router)
app.include_router(trading_results.router)


@app.get("/")
async def root():
    return {"message": "SPIMEX API"}
