from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.catalog.main import prefix

prefix = prefix + 'category'

print(prefix)


class CategoryPanelCallback(CallbackData, prefix=prefix):
    ...


class NewCategoryCallback(CallbackData, prefix=prefix + 'new'):
    ...


class EditCategoryCallback(CallbackData, prefix=prefix + 'edit'):
    ...


class EditCategoryItemCallback(CallbackData, prefix=prefix + 'edit/item'):
    id: int


class DeleteCategoryCallback(CallbackData, prefix=prefix + 'edit/delete'):
    id: int


class ConfirmDeleteCategoryCallback(CallbackData, prefix=prefix + 'edit/delete-confirm'):
    id: int
    action: bool


class EditCategoryNameCallback(CallbackData, prefix=prefix + 'edit/name'):
    id: int


class EditCategoryDescriptionCallback(CallbackData, prefix=prefix + 'edit/desc'):
    id: int
