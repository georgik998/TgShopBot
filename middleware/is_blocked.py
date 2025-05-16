from aiogram import BaseMiddleware
from typing import Any

from tg_bot.infra.database import async_session
from tg_bot.repositories.user import UserRepo


class IsUserBlockedMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler,
            event,
            data
    ) -> Any:
        tg_id = data['event_from_user'].id
        async with async_session() as session:
            is_blocked = await UserRepo(session).is_blocked(tg_id)
        if is_blocked:
            if event.message:
                await event.message.answer(
                    text='⛔️ Вы заблокированы в боте'
                )
            return
        return await handler(event, data)
