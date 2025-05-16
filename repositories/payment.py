from tg_bot.infra.database.models import Payment
from tg_bot.repositories.base import BaseRepo


class PaymentRepo(BaseRepo):
    model = Payment

    async def post(self, tg_id, system, system_id:str, amount):
        self.session.add(
            self.model(
                tg_id=tg_id,
                system=system,
                system_id=system_id,
                amount=amount
            )
        )
        await self.session.commit()
