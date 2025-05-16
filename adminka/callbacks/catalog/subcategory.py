from aiogram.filters.callback_data import CallbackData

from tg_bot.adminka.callbacks.catalog.main import prefix

prefix = prefix + 'subcategory'


# ======================== MAIN CALLBACK ========================
class SubcategoryPanelCallback(CallbackData, prefix=prefix):
    ...


class NewSubcategoryCallback(CallbackData, prefix=prefix + 'new'):
    category_id: int


# ======================== SELECT CATEGORY TO FIND SUBCAT. FOR EDIT ========================
class SelectCategoryForSubcategoryEditPanelCallback(CallbackData, prefix=prefix + 'edit/select-category'):
    id: int


class SelectCategoryForNewSubcategoryCallback(CallbackData, prefix=prefix + 'edit/select-category'):
    id: int


# ======================== EDIT SUBCATEGORY ========================
class DeleteSubcategoryCallback(CallbackData, prefix=prefix + 'edit/delete'):
    id: int
    category_id: int


class ConfirmDeleteSubcategoryCallback(CallbackData, prefix=prefix + 'edit/delete-confirm'):
    id: int
    category_id: int
    action: bool


class EditSubcategoryNameCallback(CallbackData, prefix=prefix + 'edit/name'):
    id: int
    category_id: int


class EditSubcategoryDescriptionCallback(CallbackData, prefix=prefix + 'edit/desc'):
    id: int
    category_id: int
