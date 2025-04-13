from typing import Optional

from aiohttp import ClientSession, ClientResponse
from starlette.datastructures import Headers

from api.models import HTTPMethod


class APIClient(object):
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or ""

    async def request(self, client: ClientSession, method: HTTPMethod, uri: str,
                      headers: Headers = None, **kwargs) -> ClientResponse:
        url = f'{self.base_url.strip("/")}/{uri.strip("/")}'
        return await client.request(method=method.name, url=url, headers=headers, **kwargs)
