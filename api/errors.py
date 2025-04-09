from http import HTTPStatus
from typing import Optional


class APIError(Exception):

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        self.code = code

    @staticmethod
    def handle_error(status: int, uri: str, json_response: dict, params: dict) -> None:
        if status == HTTPStatus.INTERNAL_SERVER_ERROR:
            message = f"Internal server error [params={params}]"
        else:
            message = json_response.get("message", "Unknown error")

        raise APIError(message=f"Error fetching quote data [uri={uri}]: {message}", code=status)


class QuoteDataNotFound(APIError):
    pass
