from functools import wraps
from http import HTTPStatus
from fastapi import HTTPException


def validate_symbol(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        symbol = kwargs.get("symbol")

        if not isinstance(symbol, str):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Symbol must be a string."
            )

        return await func(*args, **kwargs)

    return wrapper
