import logging.config
from contextlib import asynccontextmanager
from http import HTTPStatus

from aiohttp import ClientSession
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

from api.api_client import APIClient
from api.models import HTTPMethod
from logger.configurations import LOGGING_DICT_CONFIG
from rate_limiter_service.models import RateLimiterClient
from rate_limiter_service.rate_limiter import rate_limiter
from rate_limiter_service.settings import QUOTE_DATA_SERVICE_URL


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with ClientSession() as session:
        application.state.aiohttp_session = session
        yield

app = FastAPI(lifespan=lifespan)
rate_limiter_client = RateLimiterClient(QUOTE_DATA_SERVICE_URL)
api_client = APIClient(QUOTE_DATA_SERVICE_URL)
logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING_DICT_CONFIG)


@app.get('/rate_limiter/{symbol}')
@rate_limiter
async def get_quote_data_by_rate_limiter(request: Request, symbol: str):
    logger.info(f"Got a request to get quote data by rate limiter for symbol: {symbol}")
    response = await api_client.request(request.app.state.aiohttp_session, HTTPMethod.GET,
                                        f"/quote_data/{symbol}", headers=request.headers)
    json_response = await response.json()
    if response.status != HTTPStatus.OK:
        raise HTTPException(status_code=response.status, detail=json_response)

    return JSONResponse(status_code=HTTPStatus.OK, content={"quote_data": json_response})
