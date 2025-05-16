from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.config import back_button_style
from tg_bot.adminka.callbacks.main import NotifyChannelsCallback
from tg_bot.adminka.callbacks.notify_channels import *
from tg_bot.adminka.keyboards.main import back_to_admin_button

from tg_bot.infra.database.models import NotifyChannel

back_to_notify_channels_button = InlineKeyboardButton(text=back_button_style,
                                                      callback_data=NotifyChannelsCallback().pack())
back_to_notify_channels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style,
                                 callback_data=NotifyChannelsCallback().pack())
        ]
    ]
)

notify_channel_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🎁 Покупки', callback_data='snus'),
            # InlineKeyboardButton(text='❌ Выключить логи',
            #                      callback_data=DeleteNotifyChannelCallback(channel='purchase').pack()),
            InlineKeyboardButton(text='🧷 Изменить ссылку',
                                 callback_data=ChangeNotifyChannelCallback(channel='purchase').pack())
        ],
        [
            InlineKeyboardButton(text='🎟 Промокоды', callback_data='snus'),
            # InlineKeyboardButton(text='❌ Выключить логи',
            #                      callback_data=DeleteNotifyChannelCallback(channel='promocode').pack()),
            InlineKeyboardButton(text='🧷 Изменить ссылку',
                                 callback_data=ChangeNotifyChannelCallback(channel='promocode').pack())
        ],
        [
            InlineKeyboardButton(text='💎 Пополнения', callback_data='snus'),
            # InlineKeyboardButton(text='❌ Выключить логи',
            #                      callback_data=DeleteNotifyChannelCallback(channel='payment').pack()),
            InlineKeyboardButton(text='🧷 Изменить ссылку',
                                 callback_data=ChangeNotifyChannelCallback(channel='payment').pack())
        ],
        [
            InlineKeyboardButton(text='👤 Новые юзеры', callback_data='snus'),
            # InlineKeyboardButton(text='❌ Выключить логи',
            #                      callback_data=DeleteNotifyChannelCallback(channel='new_user').pack()),
            InlineKeyboardButton(text='🧷 Изменить ссылку',
                                 callback_data=ChangeNotifyChannelCallback(channel='new_user').pack())
        ],
        [
            back_to_admin_button
        ]
    ]
)


def build_confirm_delete(channel):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅Да',
                                     callback_data=ConfirmDeleteNotifyChannelCallback(channel=channel,
                                                                                      action=True).pack()),
                InlineKeyboardButton(text='❌Нет',
                                     callback_data=ConfirmDeleteNotifyChannelCallback(channel=channel,
                                                                                      action=False).pack())
            ],
            [
                InlineKeyboardButton(text=back_button_style, callback_data=NotifyChannelsCallback().pack())
            ]
        ]
    )
