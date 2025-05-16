from aiogram.filters.callback_data import CallbackData
from tg_bot.adminka.callbacks.main import base_prefix

base_prefix = base_prefix + 'subscribe-channels'


class SubscribeChannelDeleteCallback(CallbackData, prefix=base_prefix + 'delete'):
    id: int


class SubscribeChannelConfirmDeleteCallback(CallbackData, prefix=base_prefix + 'delete-confirm'):
    id: int
    delete: bool


class SubscribeChannelNewCallback(CallbackData, prefix=base_prefix + 'new'):
    ...
