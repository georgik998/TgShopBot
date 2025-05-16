from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'admin'


class NewAdminCallback(CallbackData, prefix=prefix + 'new'):
    ...


class DeleteAdminCallback(CallbackData, prefix=prefix + 'delete'):
    id: int
