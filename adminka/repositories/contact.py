from typing import Optional, Sequence

from sqlalchemy import text, insert, select, func, update, delete

from tg_bot.infra.database.models import Contacts

from tg_bot.repositories.base import BaseRepo


class ContactsRepo(BaseRepo):
    model = Contacts
    columns = [col.name for col in model.__table__.columns]

    async def get_contacts(self) -> model:
        result = await self.session.execute(select(self.model).limit(1))
        return result.scalars().first()

    async def update(self, key: str, value: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        await self.session.execute(
            update(self.model).values({key: value})
        )
        await self.session.commit()

    async def get(self, key: str):
        if key not in self.columns:
            raise ValueError('column name not in available names')
        result = await self.session.execute(select(getattr(self.model, key)))
        return result.scalar()