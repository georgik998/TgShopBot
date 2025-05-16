from sqlalchemy import update, select, text, delete
from typing import Sequence, Optional

from tg_bot.repositories.base import BaseRepo

from tg_bot.infra.database.models import Subcategory


class SubcategoryRepo(BaseRepo):
    model = Subcategory

    async def get_category_id_by_subcategory_id(self, subcategory_id):
        res = await self.session.execute(
            select(self.model.category_id).where(
                self.model.id == subcategory_id
            )
        )
        return res.scalar_one_or_none()

    async def get_subcategories_by_category_id(self, category_id) -> Sequence[model]:
        categories = await self.session.execute(
            select(self.model).where(self.model.category_id == category_id)
        )
        return categories.scalars().all()

    async def get_subcategory_id_by_subcategory_id(self, subcategory_id) -> int:
        result = await self.session.execute(
            select(self.model.category_id).filter_by(id=subcategory_id)
        )
        return result.scalars().first()

    async def get_subcategory_id_by_name(self, name) -> Optional[int]:
        result = await self.session.execute(
            select(self.model.category_id).filter_by(name=name)
        )
        return result.scalar_one_or_none()

    async def get_subcategories(self) -> Sequence[model]:
        categories = await self.session.execute(
            select(self.model)
        )
        return categories.scalars().all()

    async def get_subcategory_id_by_name(self, name: str) -> Optional[int]:
        res = await self.session.execute(
            select(self.model.id).where(self.model.name == name)
        )
        return res.scalar_one_or_none()

    async def add_subcategory(self, name, description, category_id):
        await self.session.execute(text(
            'INSERT INTO subcategories (name,description,category_id) VALUES(:name,:description, :category_id)'
        ), {'name': name, 'description': description, 'category_id': category_id})
        await self.session.commit()

    async def delete_subcategory(self, subcategory_id):
        await self.session.execute(
            delete(self.model).where(self.model.id == subcategory_id)
        )
        await self.session.commit()

    async def update_name(self, subcategory_id, name):
        await self.session.execute(
            update(self.model).where(self.model.id == subcategory_id).values({
                'name': name
            })
        )
        await self.session.commit()

    async def update_description(self, subcategory_id, description):
        await self.session.execute(
            update(self.model).where(self.model.id == subcategory_id).values({
                'description': description
            })
        )
        await self.session.commit()
