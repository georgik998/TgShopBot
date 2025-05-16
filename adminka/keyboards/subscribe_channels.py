from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.adminka.keyboards.main import back_to_admin_button
from tg_bot.adminka.callbacks.subscribe_channels import *
from tg_bot.keyboards.main import cancel_button

from tg_bot.infra.database.models import SubscribeChannel
from typing import Sequence


def build_subscribe_channel_panel(channels: Sequence[SubscribeChannel]) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text=f"@{channel.channel_url.removeprefix('https://t.me/')}",
                callback_data="snus"
            ),
            InlineKeyboardButton(
                text="❌ Удалить",
                callback_data=SubscribeChannelDeleteCallback(id=channel.channel_id).pack()
            )
        ]
        for channel in channels
    ]
    kb += [
        [InlineKeyboardButton(text=f"Всего каналов: {len(channels)}", callback_data="snus")],
        [InlineKeyboardButton(text=f"➕ Добавить канал", callback_data=SubscribeChannelNewCallback().pack())],
        [back_to_admin_button]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def build_confirm_delete_channel(channel_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data=SubscribeChannelConfirmDeleteCallback(id=channel_id,
                                                                                                    delete=True).pack()),
                InlineKeyboardButton(text='Нет', callback_data=SubscribeChannelConfirmDeleteCallback(id=channel_id,
                                                                                                     delete=False).pack())
            ],
            [cancel_button]
        ]
    )
