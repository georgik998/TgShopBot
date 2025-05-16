from typing import Optional, Sequence

from sqlalchemy import text, insert, select, func, update, delete

from tg_bot.infra.database.models import SubscribeChannel

from tg_bot.repositories.base import BaseRepo


class SubscribeChannelRepo(BaseRepo):
    model = SubscribeChannel

    async def add(self, channel_url: str, channel_id: int):
        self.session.add(SubscribeChannel(channel_url=channel_url, channel_id=channel_id))
        await self.session.commit()

    async def get_channels(self) -> Sequence[model]:
        result = await self.session.execute(
            select(self.model)
        )
        return result.scalars().all()

    async def delete_channel(self, channel_id: int):
        await self.session.execute(
            delete(self.model).where(self.model.channel_id == channel_id)
        )
        await self.session.commit()
