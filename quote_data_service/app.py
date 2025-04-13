import logging.config
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from aiohttp import ClientSession, ClientConnectorDNSError

from logger.configurations import LOGGING_DICT_CONFIG
from quote_data_service import settings
from api.errors import APIError, QuoteDataNotFound
from quote_data_service.protector import protect
from quote_data_service.quote_data import QuoteDataClient
from quote_data_service.settings import COST_KEY
from quote_data_service.validatior import validate_symbol
from quote_data_service.dal import cache


@asynccontextmanager
async def lifespan(application: FastAPI):
    async with ClientSession() as session:
        application.state.aiohttp_session = session
        yield

app = FastAPI(lifespan=lifespan)
quote_data_client = QuoteDataClient(settings.ALPHAVANTAGE_URL)
logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING_DICT_CONFIG)


@app.get('/total_cost')
async def get_total_cost():
    logger.info("Got a request to get total cost since last reset")
    total_cost = await cache.get_cached_raw(COST_KEY)
    return JSONResponse(status_code=HTTPStatus.OK, content={"total_cost": float(total_cost or 0.0)})


@app.post('/total_cost/reset')
async def reset_total_cost():
    logger.info("Got a request to reset total cost")
    await cache.reset_cost()
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "Total cost counter reset successfully"})


@app.get('/quote_data/{symbol}')
@validate_symbol
@protect
async def get_quote_data(request: Request, symbol: str):
    logger.info(f"Got a request to get quote data for symbol: {symbol}")
    try:
        quote_data = await quote_data_client.get_quote_data(request.app.state.aiohttp_session, symbol)

    except (APIError, QuoteDataNotFound) as ex:
        logger.error(f"{type(ex).__name__} for symbol '{symbol}': {ex.message}")
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ex.message)

    except ClientConnectorDNSError as ex:
        logger.error(f"DNS connection error for symbol '{symbol}': {str(ex)}")
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(ex))

    return JSONResponse(status_code=HTTPStatus.OK, content={"quote_data": quote_data.serialize})
