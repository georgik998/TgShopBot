from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.adminka.callbacks.spam import *
from tg_bot.adminka.keyboards.main import back_to_admin_button

confirm_sms = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data=ConfirmSmsCallback(action=True).pack()),
            InlineKeyboardButton(text='Нет', callback_data=ConfirmSmsCallback(action=False).pack())
        ],
        [
            back_to_admin_button
        ]
    ]
)
