from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.main import base_prefix

base_prefix = base_prefix + 'ref-links'


class EditRefLinkCallback(CallbackData, prefix=base_prefix + 'edit'):
    id: str


class NewRefLinkCallback(CallbackData, prefix=base_prefix + 'new'):
    ...


class DelRefLinkCallback(CallbackData, prefix=base_prefix + 'del'):
    id: str


class ResetRefLinkCallback(CallbackData, prefix=base_prefix + 'reset'):
    id: str


class ConfirmDelRefLinkCallback(CallbackData, prefix=base_prefix + 'del-confirm'):
    id: str
    action: bool


class ConfirmResetRefLinkCallback(CallbackData, prefix=base_prefix + 'reset-confirm'):
    id: str
    action: bool


class EditLabelRefLinKCallback(CallbackData, prefix=base_prefix + 'edit-label'):
    id: str
