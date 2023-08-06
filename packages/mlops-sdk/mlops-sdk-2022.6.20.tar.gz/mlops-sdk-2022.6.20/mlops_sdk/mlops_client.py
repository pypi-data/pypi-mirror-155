from typing import Any, Dict

import aiohttp

from mlops.config import Config


class MlopsError(Exception):
    """
    Exception class for Mlops Client.
    """

    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code
        self.msg = msg


class MlopsClient:
    """
    Super class for clients.
    """

    def __init__(self, config: Config):
        self.url = config.URL
        self.env = config.ENV
        self.apikey_header = {"x-api-key": config.APIKEY}

    async def _request(
        self, method: str, url: str, headers: Dict[str, Any] = None, data: Any = None, params=None
    ) -> Any:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=f"{self.url}{'' if url.startswith('/') else '/'}{url}",
                headers={**self.apikey_header, **headers} if headers else self.apikey_header,
                json=data,
                params=params,
            ) as response:
                try:
                    body = await response.json()
                    if not response.ok:
                        raise MlopsError(code=response.status, msg=body.get("error"))
                    return body
                except aiohttp.client_exceptions.ContentTypeError:
                    return await response.text() or None
