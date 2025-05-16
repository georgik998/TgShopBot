from aiogram.filters.callback_data import CallbackData
from typing import Optional

from tg_bot.adminka.callbacks.catalog.main import prefix

prefix = prefix + 'product'


class ProductPanelCallback(CallbackData, prefix=prefix):
    ...


# ================ NAVIGATION: select category -> subcategory for find product  ================ #
class SelectCategoryForProductCallback(CallbackData, prefix=prefix + 'select/category'):
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None


class SelectSubcategoryForProductCallback(CallbackData, prefix=prefix + 'select/subcategory'):
    subcategory_id: int


# ================ MANAGE PRODUCT ================ #
class NewProductCallback(CallbackData, prefix=prefix + 'item/new'):
    subcategory_id: int


class DeleteProductCallback(CallbackData, prefix=prefix + 'item/del'):
    product_id: int
    subcategory_id: int


class ConfirmDeleteProductCallback(CallbackData, prefix=prefix + 'item/del-confirm'):
    product_id: int
    subcategory_id: int
    action: bool


class EditProductCallback(CallbackData, prefix=prefix + 'item/edit'):
    product_id: int
    subcategory_id: int


class EditProductItem(CallbackData, prefix=prefix + 'item/edit/item'):
    product_id: int
    subcategory_id: int
    action: str
