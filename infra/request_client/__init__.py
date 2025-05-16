from typing import Optional

from aiohttp import ClientSession, ClientResponse, ClientTimeout


# import ssl
# import certifi
# from aiohttp import TCPConnector
# ssl_context = ssl.create_default_context(cafile=certifi.where())
# connector = TCPConnector(ssl=ssl_context)
# session = ClientSession(connector=connector)
class Method:
    GET: str = 'GET'
    POST: str = 'POST'
    DELETE: str = 'DELETE'
    PUT: str = 'PUT'
    PATCH: str = 'PATCH'


class RequestClient:
    session: Optional[ClientSession] = None
    timeout = ClientTimeout(total=30)

    def __init__(self):
        self.session = None

    async def __create_session(self):
        if self.session is None or self.session.closed:
            self.session = ClientSession()

    async def __close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def request(
            self,
            url: str,
            method: str = 'GET',
            **kwargs
    ) -> ClientResponse:
        """
        Отправка запроса с нужными параметрами
        на необходимый адрес
        :param url: str
        :param method: str, default GET
        :param kwargs:
        :return: dict
        """
        await self.__create_session()
        response = await self.session.request(method=method, url=url, **kwargs)
        # await self.__close_session()
        return response
