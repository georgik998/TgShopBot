from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.config import back_button_style

from tg_bot.adminka.callbacks.main import AdminPanelCallback,AdminCallback
from tg_bot.adminka.callbacks.admin import *

from typing import Sequence
from tg_bot.infra.database.models import User

back_to_admin_manage = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=AdminCallback().pack())
        ]
    ]
)

back_to_admin_manage_button = InlineKeyboardButton(text=back_button_style, callback_data=AdminCallback().pack())


def build_admins_panel(admins: Sequence[User]):
    kb = [
        [
            InlineKeyboardButton(text=f'№{i} | ' + str(admin), callback_data='snus'),
            InlineKeyboardButton(text='❌ Удалить', callback_data=DeleteAdminCallback(id=admin).pack())
        ]
        for i, admin in enumerate(admins,1)
    ]
    kb += [
        [InlineKeyboardButton(text='Добавить админа', callback_data=NewAdminCallback().pack())],
        [InlineKeyboardButton(text=back_button_style, callback_data=AdminPanelCallback().pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
