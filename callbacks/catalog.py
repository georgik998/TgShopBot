from aiogram.filters.callback_data import CallbackData
from typing import Optional


class CategoryCallback(CallbackData, prefix='catalog-category'):
    id: int


class SubcategoryCallback(CallbackData, prefix='catalog-subcategory'):
    id: int


class ProductCallback(CallbackData, prefix='catalog-product'):
    id: int


class SelectBuyProductMethodCallback(CallbackData, prefix='catalog-product-select-method'):
    id: int
    promocode: Optional[str] = None


class BuyProductCallback(CallbackData, prefix='catalog-product-buy'):
    id: int
    promocode: Optional[str] = None


class BuyProductWithPaymentSystem(CallbackData, prefix='catalog-product-pay-system-buy'):
    product_id: int
    amount: str
    promocode: Optional[str] = None
    system: str


class ActivePromocodeBuyProduct(CallbackData, prefix='catalog-product-buy-promocode'):
    id: int
