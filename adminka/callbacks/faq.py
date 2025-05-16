from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'faq'


class FaqItemCallback(CallbackData, prefix=prefix + 'item'):
    id: int


class DelFaqItemCallback(CallbackData, prefix=prefix + 'item/del'):
    id: int


class ConfirmDelFaqItemCallback(CallbackData, prefix=prefix + 'item/del/confirm'):
    id: int
    action: bool


class NewFaqCallback(CallbackData, prefix=prefix + 'new'):
    ...
