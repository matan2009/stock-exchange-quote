import redis.asyncio as redis

from quote_data_service.settings import REDIS_HOST, REDIS_PORT, QUERY_COST, COST_KEY

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


async def get_cached_raw(key: str) -> str:
    return await redis_client.get(key)


async def set_quote_data(key: str, ttl: int, data: str):
    await redis_client.setex(key, ttl, data)


async def increment_cost(key: str):
    await redis_client.incrbyfloat(key, QUERY_COST)


async def reset_cost():
    await redis_client.set(COST_KEY, 0.0)
