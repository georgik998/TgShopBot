from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.keyboards.main import back_to_admin_button
from tg_bot.config import back_button_style

from tg_bot.adminka.callbacks.promocodes import *
from tg_bot.adminka.callbacks.main import PromocodeCallback

from tg_bot.infra.database.models import Promocode
from typing import Sequence

back_to_promocode_panel = InlineKeyboardButton(text=back_button_style, callback_data=PromocodeCallback().pack())


def build_promocode_panel(promocodes: Sequence[Promocode]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(text=promo.name,
                                                     callback_data=PromocodeItemCallback(
                                                         name=promo.name).pack())
                            ] for promo in promocodes
                        ] + [
                            [
                                InlineKeyboardButton(text='➕ Новый промокод',
                                                     callback_data=NewPromocodeCallback().pack())
                            ],
                            [
                                back_to_admin_button
                            ]
                        ]
    )


def build_promocode_item_panel(promocode):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить', callback_data=DelPromocodeCallback(name=promocode).pack())
            ],
            [
                back_to_promocode_panel
            ]
        ]
    )


def build_confirm_del_promocode(promocode):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Да',
                                     callback_data=ConfirmDelPromocode(name=promocode, action=True).pack()),
                InlineKeyboardButton(text='❌ Нет',
                                     callback_data=ConfirmDelPromocode(name=promocode, action=False).pack()),
            ],
            [
                InlineKeyboardButton(text=back_button_style, callback_data=PromocodeItemCallback(name=promocode).pack())
            ],
        ]
    )


back_to_promo_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            back_to_promocode_panel
        ]
    ]
)

promocode_type_select = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Бесплатный баланс', callback_data=PromocodeTypeCallback(type='balance').pack())
        ],
        [
            InlineKeyboardButton(text='Скидка на покупку фиксированная',
                                 callback_data=PromocodeTypeCallback(type="discount_fix").pack())
        ],
        [
            InlineKeyboardButton(text='Скидка на покупку процент',
                                 callback_data=PromocodeTypeCallback(type="discount_percent").pack())
        ],
        [
            back_to_promocode_panel
        ],

    ]
)


def back_to_promo_item_panel(promocode):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back_button_style, callback_data=PromocodeItemCallback(name=promocode).pack())
            ]
        ]
    )
