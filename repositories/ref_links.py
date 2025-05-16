from typing import Optional, Sequence, List

from sqlalchemy import text, insert, select, func, update, delete

from tg_bot.infra.database.models import RefLink

from tg_bot.repositories.base import BaseRepo


class RefLinkRepo(BaseRepo):
    model = RefLink

    async def add_activation(self, id: str):
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(invited=self.model.invited + 1)
        )
        await self.session.commit()

    async def add_deposit(self, id: str, deposit: float):
        await self.session.execute(
            update(self.model).where(self.model.id == id).values(income=self.model.income + deposit)
        )
        await self.session.commit()

    async def is_exist(self, ref_link: str) -> bool:
        res = await self.session.execute(
            select(self.model.id).where(self.model.id == ref_link)
        )
        return bool(res.scalar_one_or_none())
