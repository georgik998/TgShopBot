from typing import Optional, Sequence
from decimal import Decimal

from sqlalchemy import text, insert, select, func, update
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from tg_bot.infra.database.models import User, UserPurchases, UserPromocodes

from tg_bot.repositories.base import BaseRepo

from tg_bot.utils import *


class UserRepo(BaseRepo):
    model = User

    # ================== GET ================
    async def is_admin(self, tg_id: int) -> bool:
        res = await self.session.execute(
            select(self.model.is_admin).where(self.model.tg_id == tg_id)
        )
        return bool(res.scalar_one_or_none())

    async def get_user(self, tg_id: int) -> Optional[model]:
        result = await self.session.execute(
            select(self.model).where(self.model.tg_id == tg_id)
        )
        user = result.scalars().one_or_none()
        return user

    async def is_blocked(self, tg_id: int) -> bool:
        is_blocked = await self.session.execute(
            select(self.model.is_blocked).where(self.model.tg_id == tg_id)
        )
        is_blocked = is_blocked.scalars().one_or_none()
        return is_blocked

    async def get_referral_balance(self, tg_id: int) -> float:
        res = await self.session.execute(
            select(self.model.referral_balance).where(self.model.tg_id == tg_id)
        )
        return round_number(res.scalars().one_or_none())

    async def count_referrals(self, father_id: int) -> int:
        res = await self.session.execute(
            select(func.count(self.model.tg_id))
            .where(self.model.father_id == father_id)
        )
        return res.scalar_one_or_none() or 0

        # ================== POST ================

    async def post_user(self, tg_id: int, father_id: int = None, ref_link_id: str = None) -> bool:
        result = await self.session.execute(
            text('INSERT INTO users (tg_id, father_id, is_ref_link) '
                 'VALUES (:tg_id, :father_id, :is_ref_link) '
                 'ON CONFLICT (tg_id) DO NOTHING '
                 'RETURNING TRUE'),
            {'tg_id': tg_id, 'father_id': father_id, 'is_ref_link': ref_link_id}
        )
        await self.session.commit()
        return bool(result.first())

    # ================== PUT ================
    async def update_balance(self, tg_id: int, balance_delta: float):
        balance_delta = Decimal(str(balance_delta))
        await self.session.execute(
            update(self.model).where(self.model.tg_id == tg_id).values({
                'balance': self.model.balance + balance_delta
            })
        )
        await self.session.commit()

    async def update_referral_balance(self, tg_id: int, balance_delta: float):
        balance_delta = Decimal(str(balance_delta))
        await self.session.execute(
            update(self.model).where(self.model.tg_id == tg_id).values(
                referral_balance=self.model.referral_balance + balance_delta
            )
        )
        await self.session.commit()


class UserPurchasesRepo(BaseRepo):
    model = UserPurchases

    async def get_purchases(self, tg_id: int) -> Sequence[model]:
        result = await self.session.execute(
            select(self.model).where(self.model.tg_id == tg_id)
        )
        return result.scalars().all()

    async def get_purchases_amount(self, tg_id: int) -> float:
        result = await self.session.execute(
            select(func.sum(self.model.amount)).where(self.model.tg_id == tg_id)
        )
        return result.scalar() or 0.0

    async def get_purchases_count(self, tg_id: int) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model).where(self.model.tg_id == tg_id)
        )
        return result.scalar_one() or 0

    async def get_purchase(self, purchase_id: str) -> model:
        result = await self.session.execute(select(self.model).filter(self.model.id == purchase_id))
        purchase = result.scalars().one_or_none()
        return purchase

    async def add_purchase(self, tg_id: int, amount: float, name: str, content: str) -> str:
        purchase = self.model(
            tg_id=tg_id,
            amount=amount,
            name=name,
            content=content
        )
        self.session.add(purchase)
        await self.session.commit()
        return purchase.id


class UserPromocodeRepo(BaseRepo):
    model = UserPromocodes

    async def add_promo(self, tg_id: int, promo: str):
        # try:
        #     self.session.add(self.model(tg_id=tg_id, promocode=promo))
        #     await self.session.commit()
        # except IntegrityError or PendingRollbackError:  # если промик был последний
        #     pass
        self.session.add(self.model(tg_id=tg_id, promocode=promo))
        await self.session.commit()

    async def check_promo(self, tg_id: int, promo: str) -> bool:
        result = await self.session.execute(
            select(self.model).filter(self.model.tg_id == tg_id, self.model.promocode == promo)
        )
        return result.scalar() is not None
