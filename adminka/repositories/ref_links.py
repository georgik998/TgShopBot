from typing import Optional, Sequence, List

from sqlalchemy import text, insert, select, func, update, delete

from tg_bot.infra.database.models import RefLink

from tg_bot.repositories.base import BaseRepo


class RefLinkRepo(BaseRepo):
    model = RefLink

    async def get_all(self) -> List[model]:
        res = await self.session.execute(
            select(
                self.model
            )
        )
        return list(res.scalars().all())

    async def get_by_id(self, id: str) -> Optional[model]:
        res = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return res.scalar_one_or_none()

    async def patch_label(self, id: str, label: str):
        await self.session.execute(
            update(
                self.model
            ).where(
                self.model.id == id
            ).values({
                'label': label
            })
        )
        await self.session.commit()

    async def delete_by_id(self, id: str):
        await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()

    async def delete_statistic_by_id(self, id: str):
        await self.session.execute(
            update(self.model).where(self.model.id == id).values({
                'invited': 0,
                'income': 0
            })
        )
        await self.session.commit()

    async def post(self, label: Optional[str] = '-') -> int:
        result = await self.session.execute(
            text('INSERT INTO ref_links (label) '
                 'VALUES (:label) '
                 'RETURNING id'),
            {'label': label}
        )
        await self.session.commit()
        return result.scalars().first()
