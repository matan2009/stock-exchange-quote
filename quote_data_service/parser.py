import logging
from datetime import datetime

from api.errors import QuoteDataNotFound
from quote_data_service.models import QuoteData

logger = logging.getLogger(__name__)


class ParserService:

    @classmethod
    def parse_quote_data(cls, global_quote: dict, symbol: str) -> QuoteData:
        if not global_quote:
            raise QuoteDataNotFound(message=f"Quote Data not found [symbol={symbol}]")

        return QuoteData(symbol=global_quote["01. symbol"], update_time=datetime.now(),
                         price=float(global_quote["05. price"]),
                         change_percent=global_quote["10. change percent"])

