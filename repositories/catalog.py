from sqlalchemy import update, select
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

    async def get(self, category_id) -> model:
        res = await self.session.execute(
            select(self.model).where(self.model.id == category_id)
        )
        return res.scalar_one_or_none()


class SubcategoryRepo(BaseRepo):
    model = Subcategory

    async def get(self, subcategory_id) ->model:
        res = await self.session.execute(
            select(self.model).where(self.model.id == subcategory_id)
        )
        return res.scalar_one_or_none()

    async def get_subcategories_by_category_id(self, category_id) -> Sequence[model]:
        categories = await self.session.execute(
            select(self.model).where(self.model.category_id == category_id)
        )
        return categories.scalars().all()

    async def get_category_id_by_subcategory_id(self, subcategory_id) -> int:
        result = await self.session.execute(
            select(self.model.category_id).filter_by(id=subcategory_id)
        )
        return result.scalars().first()


class ProductRepo(BaseRepo):
    model = Product

    async def get_products_by_subcategory_id(self, subcategory_id) -> Sequence[model]:
        categories = await self.session.execute(
            select(self.model).where(self.model.subcategory_id == subcategory_id)
        )
        return categories.scalars().all()

    async def get_product(self, product_id) -> model:
        product = await self.session.execute(
            select(self.model).where(self.model.id == product_id)
        )
        product = product.scalars().one_or_none()
        return product

    async def get_product_content(self, product_id) -> Optional[str]:
        result = await self.session.execute(select(self.model).filter(self.model.id == product_id))
        product = result.scalar_one_or_none()

        if product and product.content:
            last_element = product.content[-1]

            product.content.pop()

            await self.session.execute(
                update(self.model)
                .where(self.model.id == product_id)
                .values(content=product.content)
            )
            await self.session.commit()

            return last_element
        return None
