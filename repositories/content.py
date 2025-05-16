from sqlalchemy import text, select, update, delete

from typing import Sequence

from tg_bot.repositories.base import BaseRepo

from tg_bot.infra.database.models import TextTable, Contacts, Faq, Promocode, SubscribeChannel, Banner, NotifyChannel


class TextRepo(BaseRepo):
    text_model = TextTable
    columns = [col.name for col in text_model.__table__.columns]

    async def get_text(self, key: str):
        if key not in self.columns:
            raise ValueError('text-column name not in available names')
        result = await self.session.execute(select(getattr(self.text_model, key)))
        return result.scalar()

    async def update_text(self, key: str, text_message: str):
        if key not in self.columns:
            raise ValueError('text-column name not in available names')
        self.session.add(TextTable(**{key: text_message}))
        await self.session.commit()


class BannerRepo(BaseRepo):
    text_model = Banner
    columns = [col.name for col in text_model.__table__.columns]

    async def get(self, key) -> str:
        if key not in self.columns:
            raise ValueError('text-column name not in available names')
        result = await self.session.execute(select(getattr(self.text_model, key)))
        return result.scalar()


class ContactsRepo(BaseRepo):
    model = Contacts
    columns = [col.name for col in model.__table__.columns]

    async def get_contacts(self) -> model:
        result = await self.session.execute(select(self.model).limit(1))
        return result.scalars().first()


class FaqRepo(BaseRepo):
    model = Faq

    async def get_faq(self):
        result = await self.session.execute(select(self.model))
        return result.scalars()

    async def get_answer(self, question_id):
        result = await self.session.execute(
            select(self.model.answer).where(self.model.id == question_id)
        )
        return result.scalar_one_or_none()


class PromocodeRepo(BaseRepo):
    model = Promocode

    async def get_promocode_by_name(self, promocode):
        result = await self.session.execute(
            select(self.model).where(self.model.name == promocode)
        )
        return result.scalar_one_or_none()

    async def post_activation(self, promocode):
        await self.session.execute(
            update(self.model)
            .where(self.model.name == promocode)
            .values(activations=Promocode.activations - 1)
        )

        await self.session.execute(
            delete(self.model)
            .where(self.model.name == promocode)
            .where(self.model.activations - 1 <= 0)
        )
        await self.session.commit()


class SubscribeChannelRepo(BaseRepo):
    model = SubscribeChannel

    async def get_channels(self) -> Sequence[model]:
        result = await self.session.execute(
            select(self.model)
        )
        return result.scalars().all()


class NotifyChannelRepo(BaseRepo):
    model = NotifyChannel
    columns = [col.name for col in model.__table__.columns]

    async def get_channels(self) -> model:
        result = await self.session.execute(
            select(self.model)
        )
        return result.scalars().first()

    async def get_channel(self, key) -> int:
        result = await self.session.execute(
            select(self.model)
        )
        return getattr(result.scalars().first(), key)
