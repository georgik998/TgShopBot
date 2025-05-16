from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.keyboards.main import back_to_admin_button
from tg_bot.config import back_button_style

from tg_bot.adminka.callbacks.faq import *
from tg_bot.adminka.callbacks.main import FaqCallback

from tg_bot.infra.database.models import Faq
from typing import Sequence

back_to_faq = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=FaqCallback().pack()),
        ]
    ]
)


def build_faq_panel(faq_info: Sequence[Faq]):
    kb = []
    for question in faq_info:
        kb.append([
            InlineKeyboardButton(text=question.question, callback_data=FaqItemCallback(id=question.id).pack())
        ])
    kb += [
        [
            InlineKeyboardButton(text='➕ Добавить новый вопрос', callback_data=NewFaqCallback().pack())
        ],
        [
            back_to_admin_button
        ]
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=kb
    )


def build_faq_item_panel(faq_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='❌ Удалить', callback_data=DelFaqItemCallback(id=faq_id).pack()),
            ],
            [
                InlineKeyboardButton(text=back_button_style, callback_data=FaqCallback().pack()),
            ]
        ]
    )


def build_faq_item_del_confirm(faq_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Да', callback_data=ConfirmDelFaqItemCallback(id=faq_id, action=True).pack()),
                InlineKeyboardButton(text='❌ Нет',
                                     callback_data=ConfirmDelFaqItemCallback(id=faq_id, action=False).pack()),
            ],
            [
                InlineKeyboardButton(text=back_button_style, callback_data=FaqItemCallback(id=faq_id).pack()),
            ]
        ]
    )


def back_to_faq_panel(faq_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back_button_style, callback_data=FaqItemCallback(id=faq_id).pack()),
            ]
        ]
    )
