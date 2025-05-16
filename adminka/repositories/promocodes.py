from sqlalchemy import text, select, update, delete

from typing import Sequence, Union

from tg_bot.repositories.base import BaseRepo

from tg_bot.infra.database.models import Promocode


class PromocodeRepo(BaseRepo):
    model = Promocode

    async def get_promocodes(self):
        res = await self.session.execute(
            select(self.model)
        )
        return res.scalars().all()

    async def get_promocode_by_name(self, name: str) -> Union[model]:
        res = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return res.scalar_one_or_none()

    async def add_promocode(self, name, quantity, type, content):
        self.session.add(self.model(
            name=name,
            activations = quantity,
            type=type,
            content=content
        ))
        await self.session.commit()
    async def del_promocode(self, promocode):
        await self.session.execute(
            delete(self.model).where(self.model.name == promocode)
        )
        await self.session.commit()
