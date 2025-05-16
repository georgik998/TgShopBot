from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.callbacks.main import ContactCallback
from tg_bot.adminka.callbacks.contact import *
from tg_bot.adminka.keyboards.main import back_to_admin_button

from tg_bot.config import back_button_style

contact_manage = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💂‍♀️ Саппорт', callback_data=EditContactCallback(contact='support').pack())
        ],
        [
            InlineKeyboardButton(text='👑 Владелец', callback_data=EditContactCallback(contact='owner').pack())
        ],
        [
            InlineKeyboardButton(text='📰 Новости', callback_data=EditContactCallback(contact='news').pack())
        ],
        [
            InlineKeyboardButton(text='👍 Отзывы', callback_data=EditContactCallback(contact='review').pack())
        ],
        [
            back_to_admin_button
        ]
    ]
)

back_to_contact_manage = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=ContactCallback().pack())
        ]
    ]
)


def test_url(url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(text='Новая ссылка', url=url)
                            ]
                        ] + back_to_contact_manage.inline_keyboard
    )
