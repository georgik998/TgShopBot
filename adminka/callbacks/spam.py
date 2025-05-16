from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'spam'


class ConfirmSmsCallback(CallbackData, prefix=prefix + 'confirm'):
    action: bool
