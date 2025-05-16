from typing import Optional, Sequence
from decimal import Decimal

from sqlalchemy import text, insert, select, func, update

from tg_bot.infra.database.models import User, UserPurchases

from tg_bot.repositories.base import BaseRepo

from datetime import datetime, timedelta


class UserRepo(BaseRepo):
    model = User

    async def post_user(self, tg_id: int, father_id: int = None) -> bool:
        result = await self.session.execute(
            text('INSERT INTO users (tg_id, father_id) '
                 'VALUES (:tg_id, :father_id) '
                 'ON CONFLICT (tg_id) DO NOTHING '
                 'RETURNING TRUE'),
            {'tg_id': tg_id, 'father_id': father_id}
        )
        await self.session.commit()
        return bool(result.first())

    # ================== GET ================
    async def update_balance(self, tg_id: int, balance_delta: float):
        balance_delta = Decimal(str(balance_delta))
        await self.session.execute(
            update(self.model).where(self.model.tg_id == tg_id).values(balance=self.model.balance + balance_delta)
        )
        await self.session.commit()

    async def get_user(self, tg_id) -> model:
        res = await self.session.execute(
            select(self.model).where(self.model.tg_id == tg_id)
        )
        return res.scalars().first()

    async def get_all(self) -> Sequence[model]:
        res = await self.session.execute(
            select(self.model)
        )
        return res.scalars().all()

    async def is_admin(self, tg_id: int) -> bool:
        result = await self.session.execute(
            select(self.model).where(self.model.tg_id == tg_id)
        )
        user = result.scalars().one_or_none()
        if user:
            return user.is_admin
        return False

    async def get_admins(self):
        res = await self.session.execute(
            select(self.model.tg_id).where(self.model.is_admin == True)
        )
        return res.scalars().all()

    async def ban_user(self, tg_id):
        await self.session.execute(
            update(self.model)
            .where(self.model.tg_id == tg_id)
            .values(is_blocked=True)
        )
        await self.session.commit()

    async def unban_user(self, tg_id):
        await self.session.execute(
            update(self.model)
            .where(self.model.tg_id == tg_id)
            .values(is_blocked=False)
        )
        await self.session.commit()

    async def set_admin(self, tg_id, is_admin: bool):
        await self.session.execute(
            update(self.model).where(
                self.model.tg_id == tg_id
            ).values(is_admin=is_admin)
        )
        await self.session.commit()

    # ================== GET ================
    async def get_statistic(self):
        today = datetime.utcnow().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # Готовим запросы
        total_users_query = select(func.count()).select_from(self.model)
        today_users_query = select(func.count()).where(func.date(self.model.registration_date) == today)
        week_users_query = select(func.count()).where(self.model.registration_date >= week_ago)
        month_users_query = select(func.count()).where(self.model.registration_date >= month_ago)
        last_registration_query = select(func.max(self.model.registration_date))
        blocked_users_query = select(func.count()).where(self.model.is_blocked == True)
        total_balance_query = select(func.sum(self.model.balance))

        # Выполняем запросы
        total_users = (await self.session.execute(total_users_query)).scalar_one()
        today_users = (await self.session.execute(today_users_query)).scalar_one()
        week_users = (await self.session.execute(week_users_query)).scalar_one()
        month_users = (await self.session.execute(month_users_query)).scalar_one()
        last_registration = (await self.session.execute(last_registration_query)).scalar_one()
        blocked_users = (await self.session.execute(blocked_users_query)).scalar_one()
        total_balance = (await self.session.execute(total_balance_query)).scalar_one()

        return {
            "total_users": total_users,
            "today_users": today_users,
            "week_users": week_users,
            "month_users": month_users,
            "last_registration": last_registration,
            "blocked_users": blocked_users,
            "blocked_users_percent": round(blocked_users / total_users * 100, 1) if blocked_users != 0 else 0,
            "total_balance": float(total_balance) if total_balance else 0.0,
        }


class UserPurchasesRepo(BaseRepo):
    model = UserPurchases

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
