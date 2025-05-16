from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.callbacks.catalog.category import *
from tg_bot.adminka.callbacks.main import CatalogCallback

from tg_bot.adminka.config import back_button_style

from tg_bot.infra.database.models import Category
from typing import Sequence

category_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='➕ Добавить новую', callback_data=NewCategoryCallback().pack()),
            InlineKeyboardButton(text='✏️ Управление текущими', callback_data=EditCategoryCallback().pack())
        ],
        [
            InlineKeyboardButton(text=back_button_style, callback_data=CatalogCallback().pack())
        ]
    ]
)

back_to_category_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=CategoryPanelCallback().pack())
        ]
    ]
)

back_to_category_edit_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=EditCategoryCallback().pack())
        ]
    ]
)


def build_category_manage_panel(data: Sequence[Category]):
    kb = []
    for category in data:
        kb.append([
            InlineKeyboardButton(text=category.name, callback_data='snus'),
            InlineKeyboardButton(text='❌', callback_data=DeleteCategoryCallback(id=category.id).pack()),
            InlineKeyboardButton(text='✏️', callback_data=EditCategoryNameCallback(id=category.id).pack()),
            InlineKeyboardButton(text='📖️', callback_data=EditCategoryDescriptionCallback(id=category.id).pack()),
        ])
    kb.append([InlineKeyboardButton(text=back_button_style, callback_data=CategoryPanelCallback().pack())])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def confirm_delete_category(category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да, я уверен',
                                     callback_data=ConfirmDeleteCategoryCallback(id=category_id, action=True).pack()),
                InlineKeyboardButton(text='✅Отменить',
                                     callback_data=ConfirmDeleteCategoryCallback(id=category_id, action=False).pack()),
            ],
            [
                InlineKeyboardButton(text=back_button_style, callback_data=EditCategoryCallback().pack())
            ]
        ]
    )
