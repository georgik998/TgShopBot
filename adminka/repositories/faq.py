from sqlalchemy import text, select, update, delete

from typing import Sequence

from tg_bot.repositories.base import BaseRepo

from tg_bot.infra.database.models import Faq


class FaqRepo(BaseRepo):
    model = Faq

    async def del_faq(self, question_id):
        await self.session.execute(
            delete(self.model).where(self.model.id == question_id)
        )
        await self.session.commit()

    async def get_faq(self):
        result = await self.session.execute(select(self.model))
        return result.scalars()

    async def get_faq_by_id(self, faq_id) -> model:
        result = await self.session.execute(select(self.model).where(self.model.id == faq_id))
        return result.scalar_one_or_none()

    async def get_answer(self, question_id):
        result = await self.session.execute(
            select(self.model.answer).where(self.model.id == question_id)
        )
        return result.scalar_one_or_none()

    async def edit_question(self, question_id, question_text):
        await self.session.execute(
            update(self.model).where(self.model.id == question_id).values({
                'question': question_text
            })
        )

    async def edit_answer(self, question_id, answer_text):
        await self.session.execute(
            update(self.model).where(self.model.id == question_id).values({
                'answer': answer_text
            })
        )

    async def add_faq(self, question, answer):
        self.session.add(self.model(
            question=question,
            answer=answer
        ))
        await self.session.commit()
