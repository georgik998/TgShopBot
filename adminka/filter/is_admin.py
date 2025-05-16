from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from typing import Union

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.user import UserRepo


class IsAdminFilter(BaseFilter):

    def __init__(self, *keys):
        self.keys = set(keys)

    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        user_id = message.from_user.id
        async with async_session() as session:
            return await UserRepo(session).is_admin(user_id)
