from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

prefix = base_prefix + 'content'


class TextEditCallback(CallbackData, prefix=prefix + 'text'):
    ...


class BannerEditCallback(CallbackData, prefix=prefix + 'media'):
    ...


class TextFieldCallback(CallbackData, prefix=prefix + 'text-field'):
    field: str


class BannerFieldCallback(CallbackData, prefix=prefix + 'banner-field'):
    field: str


class TextFieldConfirmCallback(CallbackData, prefix=prefix + 'text-field-confirm'):
    action: bool


class BannerFieldConfirmCallback(CallbackData, prefix=prefix + 'banner-field-confirm'):
    action: bool
