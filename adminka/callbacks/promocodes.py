from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix


class PromocodeItemCallback(CallbackData, prefix=base_prefix + 'item'):
    name: str


class NewPromocodeCallback(CallbackData, prefix=base_prefix + 'new'):
    ...


class PromocodeTypeCallback(CallbackData, prefix=base_prefix + 'type'):
    type: str


class DelPromocodeCallback(CallbackData, prefix=base_prefix + 'del'):
    name: str


class ConfirmDelPromocode(CallbackData, prefix=base_prefix + 'del/confirm'):
    name: str
    action: bool
