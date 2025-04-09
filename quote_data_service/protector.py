from functools import wraps
from fastapi import Request, HTTPException
import jwt
from http import HTTPStatus

from quote_data_service.settings import ALGORITHM, SECRET_KEY


def protect(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.token_payload = payload
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token is invalid or expired")

        return await func(request, *args, **kwargs)

    return wrapper
