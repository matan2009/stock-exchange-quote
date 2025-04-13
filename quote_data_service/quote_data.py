from http import HTTPStatus
from typing import Dict
import json
import pytz
from datetime import datetime
from aiohttp import ClientSession

from api.api_client import APIClient
from api.models import HTTPMethod
from quote_data_service.dal import cache
from api.errors import APIError
from quote_data_service.models import QuoteData
from quote_data_service.parser import ParserService
from quote_data_service.settings import GLOBAL_QUOTE, API_KEY, ONE_HOUR, TEN_MINUTES, TWENTY_MINUTES, RATIO_THRESHOLD, \
    COST_KEY


class QuoteDataClient(APIClient):
    def __init__(self, base_url: str = "", max_retry: int = 3):
        super(QuoteDataClient, self).__init__(base_url)
        self._max_retry = max_retry

    @staticmethod
    def _get_quote_data_params(symbol: str) -> Dict[str, str]:
        return dict(function=GLOBAL_QUOTE, symbol=symbol, apikey=API_KEY)

    @staticmethod
    def _is_trading_hours() -> bool:
        nyc = pytz.timezone("America/New_York")
        now_nyc = datetime.now(nyc).time()
        return datetime.strptime("10:00", "%H:%M").time() <= now_nyc <= datetime.strptime("17:00", "%H:%M").time()

    def _determine_ttl(self, data: dict) -> int:
        high = float(data.get("03. high", 0))
        low = float(data.get("04. low", 0))
        ratio = high / low if low else 0
        if not ratio or not self._is_trading_hours():
            return ONE_HOUR

        if ratio > RATIO_THRESHOLD:
            return TEN_MINUTES
        return TWENTY_MINUTES

    async def _fetch_quote_data(self, client: ClientSession, symbol: str) -> dict:
        uri = "/query"
        params = self._get_quote_data_params(symbol)

        response = await self.request(client, HTTPMethod.GET, uri, params=params)
        json_response = await response.json()

        if response.status == HTTPStatus.OK:
            if "Error Message" in json_response:
                raise APIError(message=json_response["Error Message"])
            return json_response.get("Global Quote", {})

        APIError.handle_error(response.status, uri, json_response, params)

    async def get_quote_data(self, client: ClientSession, symbol: str) -> QuoteData:
        stock_key = f"stock:{symbol.upper()}"
        cached_raw = await cache.get_cached_raw(stock_key)

        if cached_raw:
            cached_quote_data = json.loads(cached_raw)
            return ParserService.parse_quote_data(cached_quote_data, symbol)

        fresh_quote_data = await self._fetch_quote_data(client, symbol)
        ttl = self._determine_ttl(fresh_quote_data)
        await cache.set_quote_data(stock_key, ttl, json.dumps(fresh_quote_data))
        await cache.increment_cost(COST_KEY)
        return ParserService.parse_quote_data(fresh_quote_data, symbol)

