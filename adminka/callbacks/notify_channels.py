from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'notify_channels'


class DeleteNotifyChannelCallback(CallbackData, prefix=prefix + 'delete'):
    channel: str


class ConfirmDeleteNotifyChannelCallback(CallbackData, prefix=prefix + 'delete/confirm'):
    channel: str
    action: bool


class ChangeNotifyChannelCallback(CallbackData, prefix=prefix + 'change'):
    channel: str
