import hashlib
import json
from datetime import datetime, timedelta, time
from app.redis_cache import redis_client


def make_cache_key(base: str, params: dict) -> str:
    sorted_items = sorted(params.items())
    key_str = base + "?" + "&".join(f"{k}={v}" for k, v in sorted_items if v is not None)
    return "spimex:" + hashlib.md5(key_str.encode()).hexdigest()


def get_seconds_until_1411() -> int:
    now = datetime.now()
    target = datetime.combine(now.date(), time(14, 11))
    if now >= target:
        target += timedelta(days=1)
    return int((target - now).total_seconds())


async def get_or_set_cache(key: str, fallback_func):
    if redis_client is None:
        return await fallback_func()

    cached = await redis_client.get(key)
    if cached:
        return json.loads(cached)

    data = await fallback_func()
    await redis_client.set(key, json.dumps(data, default=str), ex=get_seconds_until_1411())
    return data
