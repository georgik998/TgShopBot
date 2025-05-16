from typing import Optional, Sequence

from sqlalchemy import text, insert, select, func, update, delete

from tg_bot.infra.database.models import TextTable, Banner
from tg_bot.repositories.base import BaseRepo


class TextRepo(BaseRepo):
    model = TextTable
    columns = [col.name for col in model.__table__.columns]

    async def update(self, key: str, value: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        await self.session.execute(
            update(self.model).values({key: value})
        )
        await self.session.commit()

    async def get_text(self, key: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        result = await self.session.execute(select(getattr(self.model, key)))
        return result.scalar()


class BannerRepo(BaseRepo):
    model = Banner
    columns = [col.name for col in model.__table__.columns]

    async def update(self, key: str, value: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        await self.session.execute(
            update(self.model).values({key: value})
        )
        await self.session.commit()

    async def get_text(self, key: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        result = await self.session.execute(select(getattr(self.model, key)))
        return result.scalar()
