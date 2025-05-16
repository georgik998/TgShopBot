from sqlalchemy import update, select, text, delete
from typing import Sequence, Optional

from tg_bot.repositories.base import BaseRepo

from tg_bot.infra.database.models import Category, Subcategory, Product


class CategoryRepo(BaseRepo):
    model = Category

    async def get_categories(self) -> Sequence[model]:
        categories = await self.session.execute(
            select(self.model)
        )
        return categories.scalars().all()

    async def get_category_id_by_name(self, name: str) -> Optional[int]:
        res = await self.session.execute(
            select(self.model.id).where(self.model.name == name)
        )
        return res.scalar_one_or_none()

    async def add_category(self, name: str, description: str):
        await self.session.execute(text(
            'INSERT INTO categories (name,description) VALUES(:name,:description)'
        ), {'name': name, "description": description})
        await self.session.commit()

    async def delete_category(self, category_id):
        await self.session.execute(
            delete(self.model).where(self.model.id == category_id)
        )
        await self.session.commit()

    async def update_name(self, category_id, name):
        await self.session.execute(
            update(self.model).where(self.model.id == category_id).values({
                'name': name
            })
        )
        await self.session.commit()

    async def patch_description(self, category_id, description):
        await self.session.execute(
            update(self.model).where(self.model.id == category_id).values({
                'description': description
            })
        )
        await self.session.commit()
