from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'contact'


class EditContactCallback(CallbackData, prefix=prefix + 'edit'):
    contact: str
