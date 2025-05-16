from sqlalchemy import (
    BigInteger, String, Text, Enum, Boolean, TIMESTAMP, DECIMAL, Integer, LargeBinary,
    ForeignKey,
    func, text
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

import enum

from datetime import datetime

from tg_bot.config import base_photo_id


class Base(AsyncAttrs, DeclarativeBase):
    pass


# ================================ CATALOG & PRODUCTS & CATEGORY TABLES ================================ #
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default='Выберите подкатегорию',
                                             server_default=text("'Выберите подкатегорию'"))


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column((ForeignKey("categories.id", ondelete="CASCADE")))
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default='Выберите товар',
                                             server_default=text("'Выберите товар'"))


product_description_max_length = 756
product_name_max_length = 128


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column((ForeignKey("subcategories.id", ondelete="CASCADE")))
    name: Mapped[str] = mapped_column(String(product_name_max_length), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(product_description_max_length), nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False)
    content: Mapped[list] = mapped_column(JSONB, nullable=False, default=[], server_default=text("'[]'"))
    photo: Mapped[str] = mapped_column(Text, nullable=False)


# ================================ BOT CONTENT & CONFIG TABLES ================================ #

class TextTable(Base):
    __tablename__ = 'texts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    start: Mapped[str] = mapped_column(Text, nullable=False, default='/start', server_default=text("'/start'"))
    info: Mapped[str] = mapped_column(Text, nullable=False, default='/info', server_default=text("'/info'"))
    faq: Mapped[str] = mapped_column(Text, nullable=False, default='/faq', server_default=text("'/faq'"))
    payment: Mapped[str] = mapped_column(Text, nullable=False, default='/payment', server_default=text("'/payment'"))


class Banner(Base):
    __tablename__ = 'banners'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    start: Mapped[str] = mapped_column(Text, nullable=False,
                                       default=base_photo_id,
                                       server_default=text(f"'{base_photo_id}'"))
    catalog: Mapped[str] = mapped_column(Text, nullable=False,
                                         default=base_photo_id,
                                         server_default=text(f"'{base_photo_id}'"))
    profile: Mapped[str] = mapped_column(Text, nullable=False,
                                         default=base_photo_id,
                                         server_default=text(f"'{base_photo_id}'"))
    info: Mapped[str] = mapped_column(Text, nullable=False,
                                      default=base_photo_id,
                                      server_default=text(f"'{base_photo_id}'"))
    payment: Mapped[str] = mapped_column(Text, nullable=False,
                                         default=base_photo_id,
                                         server_default=text(f"'{base_photo_id}'"))


class Contacts(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    review: Mapped[str] = mapped_column(Text, nullable=False, default='https://t.me/fagerewaader',
                                        server_default=text("'https://t.me/fagerewaader'"))
    news: Mapped[str] = mapped_column(Text, nullable=False, default='https://t.me/fagerewaader',
                                      server_default=text("'https://t.me/fagerewaader'"))
    support: Mapped[str] = mapped_column(Text, nullable=False, default='https://t.me/fagerewaader',
                                         server_default=text("'https://t.me/fagerewaader'"))
    owner: Mapped[str] = mapped_column(Text, nullable=False, default='https://t.me/fagerewaader',
                                       server_default=text("'https://t.me/fagerewaader'"))


class Faq(Base):
    __tablename__ = 'faq'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)


class PromocodeType(enum.Enum):
    balance = 'balance'
    discount_percent = 'discount_percent'
    discount_fix = 'discount_fix'


class Promocode(Base):
    __tablename__ = 'promocodes'
    name: Mapped[str] = mapped_column(Text, primary_key=True)
    activations: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text('0'))
    type: Mapped[PromocodeType] = mapped_column(Enum(PromocodeType), nullable=False)
    content: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False)


class NotifyChannel(Base):
    __tablename__ = 'notify_channels'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    payment: Mapped[int] = mapped_column(BigInteger, nullable=True)
    purchase: Mapped[int] = mapped_column(BigInteger, nullable=True)
    promocode: Mapped[int] = mapped_column(BigInteger, nullable=True)
    new_user: Mapped[int] = mapped_column(BigInteger, nullable=True)


class SubscribeChannel(Base):
    __tablename__ = 'subscribe_channel'
    channel_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    channel_url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class PaymentStatus(enum.Enum):
    created = 'created'
    success = 'success'
    canceled = 'canceled'


class Payment(Base):
    __tablename__ = 'payments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))
    system: Mapped[str] = mapped_column(Text, nullable=False)
    system_id: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.created,
                                                  server_default=text(f"'{PaymentStatus.created.value}'"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=func.now(),
                                                 server_default=func.now())


class RefLink(Base):
    __tablename__ = 'ref_links'
    id: Mapped[str] = mapped_column(String(8), server_default=func.generate_short_id_for_ref_links(), unique=True,
                                    nullable=False, primary_key=True)
    label: Mapped[str] = mapped_column(String(512), nullable=False, default='-', server_default=text("'-'"))
    invited: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    income: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False, default=0, server_default=text("0"))


# ================================ USERS TABLES ================================ #
class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    father_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id", ondelete="SET NULL"),
                                           nullable=True, )
    is_ref_link: Mapped[str] = mapped_column(String(8), ForeignKey("ref_links.id", ondelete="SET NULl"), nullable=True)
    balance: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False, default=0.000,
                                           server_default=text('0.000'))
    referral_balance: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False, default=0.000,
                                                    server_default=text('0.000'))
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('FALSE'))
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('FALSE'))
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=func.now(),
                                                        server_default=func.now())


class UserPurchases(Base):
    __tablename__ = 'user_purchases'

    id: Mapped[str] = mapped_column(String(12), server_default=func.generate_short_id_for_user_purchases(), unique=True,
                                    nullable=False, primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(DECIMAL(10, 3), nullable=False, )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    buy_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=func.now(),
                                               server_default=func.now())


class UserPromocodes(Base):
    __tablename__ = 'user_promocodes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id", ondelete="CASCADE"))
    promocode: Mapped[str] = mapped_column(ForeignKey("promocodes.name", ondelete="CASCADE"))
