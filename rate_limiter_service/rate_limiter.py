from functools import wraps
from http import HTTPStatus

import redis
from fastapi import HTTPException, Request

from rate_limiter_service.dal import cache
from rate_limiter_service.settings import LIMIT, TIME_FRAME


async def is_allowed(ip: str) -> bool:
    key = f"rate_limit:{ip}"

    try:
        count = await cache.increment_request_count(key)

        if count == 1:
            await cache.set_expire_time(key, TIME_FRAME)

    except redis.exceptions.ConnectionError:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Rate limiter unavailable"
        )

    if count > LIMIT:
        return False
    return True


def rate_limiter(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        ip = request.client.host
        if not await is_allowed(ip):
            raise HTTPException(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded [time_frame_in_seconds={TIME_FRAME}][limit={LIMIT}]"
            )
        return await func(request, *args, **kwargs)
    return wrapper
