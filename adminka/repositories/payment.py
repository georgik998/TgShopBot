from sqlalchemy import select, func, desc

from tg_bot.infra.database.models import Payment, PaymentStatus
from tg_bot.repositories.base import BaseRepo


class PaymentRepo(BaseRepo):
    model = Payment

    async def get_statistic(self):
        total_transactions_query = select(func.count()).select_from(self.model)
        success_transactions_query = select(func.count()).where(self.model.status == PaymentStatus.success)
        popular_system_subquery = (
            select(self.model.system, func.count().label('count'))
            .group_by(self.model.system)
            .order_by(desc('count'))
            .limit(1)
        )
        avg_amount_query = select(func.avg(self.model.amount)).where(self.model.status == PaymentStatus.success)
        max_transaction_query = (
            select(self.model.amount, self.model.tg_id).where(self.model.status == PaymentStatus.success)
            .order_by(desc(self.model.amount))
            .limit(1)
        )

        total_transactions = (await self.session.execute(total_transactions_query)).scalar_one()
        success_transactions = (await self.session.execute(success_transactions_query)).scalar_one()

        popular_system_result = await self.session.execute(popular_system_subquery)
        popular_system_row = popular_system_result.first()
        popular_system = popular_system_row[0] if popular_system_row else None

        avg_amount = (await self.session.execute(avg_amount_query)).scalar_one()

        max_transaction_result = await self.session.execute(max_transaction_query)
        max_transaction_row = max_transaction_result.first()
        max_transaction = {
            "amount": float(max_transaction_row[0]),
            "tg_id": max_transaction_row[1],
        } if max_transaction_row else {
            "amount": None,
            "tg_id": None
        }

        return {
            "total_transactions": total_transactions,
            "success_transactions": success_transactions,
            "success_transactions_percent": round(success_transactions / total_transactions * 100,
                                                  1) if total_transactions != 0 else 0,
            "popular_system": popular_system,
            "average_amount": round(float(avg_amount), 1) if avg_amount else 0.0,
            "max_transaction": max_transaction,
        }
