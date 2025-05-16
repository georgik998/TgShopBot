from sqlalchemy import update, select, delete, text, func
from typing import Sequence, Optional, List
from decimal import Decimal
from json import dumps

from tg_bot.repositories.base import BaseRepo

from tg_bot.infra.database.models import Product


class ProductRepo(BaseRepo):
    model = Product

    # ======================== GET METHODS ========================
    async def get_all(self):
        res = await self.session.execute(
            select(self.model)
        )
        return res.scalars().all()

    async def get_all_by_subcategory_id(self, subcategory_id) -> Sequence[model]:
        categories = await self.session.execute(
            select(self.model).where(self.model.subcategory_id == subcategory_id)
        )
        return categories.scalars().all()

    async def get_by_name(self, name) -> Optional[model]:
        res = await self.session.execute(
            select(self.model).where(
                self.model.name == name
            )
        )
        return res.scalar_one_or_none()

    async def get(self, product_id) -> model:
        product = await self.session.execute(
            select(self.model).where(self.model.id == product_id)
        )
        product = product.scalars().one_or_none()
        return product

    async def get_content(self, product_id) -> Optional[str]:
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

    # ======================== PATCH METHODS ========================
    async def patch(self, col, value, product_id):
        allow_columns = [
            'name', 'description', 'price', 'photo',
        ]
        column_validator = {
            'name': lambda val: val if isinstance(val, str) else (_ for _ in ()).throw(
                ValueError(f"{col} must be a string")),
            'description': lambda val: val[:1024] if isinstance(val, str) else (_ for _ in ()).throw(
                ValueError(f"{col} must be a string")),
            'price': lambda val: Decimal(str(val)) if isinstance(val, float) else (_ for _ in ()).throw(
                ValueError(f"{col} must be a float")),
            'photo': lambda val: val if isinstance(val, str) else (_ for _ in ()).throw(
                ValueError(f"{col} must be a string"))
        }
        if col not in allow_columns:
            raise KeyError('Input col not in allow_columns\n'
                           f'your column={col}\n'
                           f'allow columns={allow_columns}')

        value = column_validator[col](value)
        await self.session.execute(
            update(self.model).where(self.model.id == product_id).values({
                col: value
            })
        )

        await self.session.commit()

    # ======================== POST METHODS ========================
    async def post_content(self, product_id, content: List[str]):
        await self.session.execute(
            update(self.model).where(
                self.model.id == product_id
            ).values({
                'content': text("content || :new_content")
            }), {
                'new_content': dumps(content)
            }
        )
        await self.session.commit()

    async def post(self, subcategory_id, name, description, photo, price, content):
        self.session.add(self.model(
            subcategory_id=subcategory_id,
            name=name,
            description=description,
            photo=photo,
            price=price,
            content=content
        ))
        await self.session.commit()

    # ======================== DELETE METHODS ========================
    async def delete(self, product_id):
        await self.session.execute(
            delete(self.model).where(self.model.id == product_id)
        )
        await self.session.commit()

    async def get_statistic(self):
        total_products_query = select(func.count()).select_from(self.model)
        avg_price_query = select(func.avg(self.model.price))
        revenue_query = select(
            func.sum(
                func.coalesce(func.jsonb_array_length(self.model.content), 0) * self.model.price
            )
        )

        total_products = (await self.session.execute(total_products_query)).scalar_one()
        avg_price = (await self.session.execute(avg_price_query)).scalar_one()
        potential_revenue = (await self.session.execute(revenue_query)).scalar_one()

        return {
            "total_products": total_products,
            "average_price": round(float(avg_price), 1) if avg_price else 0.0,
            "potential_revenue": round(float(potential_revenue), 1) if potential_revenue else 0.0,
        }
