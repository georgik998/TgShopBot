from typing import Optional, Sequence

from sqlalchemy import text, insert, select, func, update, delete

from tg_bot.infra.database.models import NotifyChannel
from tg_bot.repositories.base import BaseRepo


class NotifyChannelRepo(BaseRepo):
    model = NotifyChannel
    columns = [col.name for col in model.__table__.columns]

    async def add_channel(self, key: str, channel_id: int):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        await self.session.execute(
            update(self.model).values({key: channel_id})
        )
        await self.session.commit()

    async def delete_channel(self, key: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        await self.session.execute(
            update(self.model)
            .where(getattr(self.model, key) == key)
            .values({key: None})
        )
        await self.session.commit()
