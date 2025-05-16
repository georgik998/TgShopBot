from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Sequence

from tg_bot.callbacks.payment import PaymentAmountCallback, PaymentSystemCallback
from tg_bot.callbacks.main import PaymentCallback, CatalogCallback
from tg_bot.config import back_button_style

payment_amounts = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="250₽", callback_data=PaymentAmountCallback(amount=250).pack()),
            InlineKeyboardButton(text="500₽", callback_data=PaymentAmountCallback(amount=500).pack()),
            InlineKeyboardButton(text="1000₽", callback_data=PaymentAmountCallback(amount=1000).pack()),
            InlineKeyboardButton(text="2000₽", callback_data=PaymentAmountCallback(amount=2000).pack()),
        ],
        [
            InlineKeyboardButton(text="3000₽", callback_data=PaymentAmountCallback(amount=3000).pack()),
            InlineKeyboardButton(text="4000₽", callback_data=PaymentAmountCallback(amount=4000).pack()),
            InlineKeyboardButton(text="5000₽", callback_data=PaymentAmountCallback(amount=5000).pack()),
        ],
        [
            InlineKeyboardButton(text="10000₽", callback_data=PaymentAmountCallback(amount=10000).pack()),
            InlineKeyboardButton(text="15000₽", callback_data=PaymentAmountCallback(amount=15000).pack()),
            InlineKeyboardButton(text="20000₽", callback_data=PaymentAmountCallback(amount=20000).pack()),
        ],
        [
            InlineKeyboardButton(text='▼ Другая сумма ▼', callback_data='payment_another')
        ],
        # [
        #     InlineKeyboardButton(text=back_button_style, callback_data='/start')
        # ]
    ]
)

back_to_payment = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=PaymentCallback().pack())
        ]
    ]
)


def build_back_to_payment(style: str = back_button_style):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=style, callback_data=PaymentCallback().pack())
            ]
        ]
    )


back_to_payment_button = InlineKeyboardButton(text=back_button_style, callback_data=PaymentCallback().pack())


def build_payment_system(amount):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔥 CryptoBot 🔥',
                                     callback_data=PaymentSystemCallback(amount=amount, system="cryptobot").pack()),
            ],
            [
                InlineKeyboardButton(text='Картой',
                                     callback_data=PaymentSystemCallback(amount=amount, system="aaio").pack()),
                InlineKeyboardButton(text='Картой/СБП',
                                     callback_data=PaymentSystemCallback(amount=amount, system="nicepay").pack()),

            ],
            [
                back_to_payment_button
            ]
        ]
    )


success_payment = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🛍 К покупкам!', callback_data=CatalogCallback().pack())
        ]
    ]
)


def payment(url, support_url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💠Оплатить💠', url=url)
            ],
            [
                InlineKeyboardButton(text='🛟 Техподдержка', url=support_url)
            ]
        ]
    )
