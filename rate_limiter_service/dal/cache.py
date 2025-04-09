import redis.asyncio as redis

from rate_limiter_service.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


async def get_cached_raw(key: str) -> str:
    return await redis_client.get(key)


async def increment_request_count(key: str) -> int:
    return await redis_client.incr(key)


async def set_expire_time(key: str, time_frame: int):
    await redis_client.expire(key, time_frame)
