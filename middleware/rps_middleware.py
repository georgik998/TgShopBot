from aiogram import BaseMiddleware
from typing import Any

from tg_bot.infra.log import logger
from time import time


class RpsMiddleware(BaseMiddleware):
    def __init__(self, rps_window_size: int = 10):
        super().__init__()
        self.rps_window_size = rps_window_size
        self.requests = 0
        self.last_update = time()
        self.max_requests = 0

    async def __call__(
            self,
            handler,
            event,
            data
    ) -> Any:
        current_time = time()
        if current_time - self.last_update >= self.rps_window_size:
            if self.requests >= self.max_requests:
                logger.warn(f'New max Request per {self.rps_window_size} seconds = {self.requests}')
                self.max_requests = self.requests
            self.last_update = time()
            self.requests = 0
        self.requests += 1
        return await handler(event, data)
