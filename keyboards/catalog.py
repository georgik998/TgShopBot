from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton
from typing import Sequence, Union, Optional
from tg_bot.infra.database.models import Category, Subcategory, Product
from tg_bot.callbacks.catalog import *
from tg_bot.callbacks.profile import PurchaseHistoryCallback
from tg_bot.callbacks.main import CatalogCallback, ProfileCallback

from tg_bot.config import back_button_style

from tg_bot.utils import *


def build_catalog_page(data: Sequence[Union[Category, Subcategory]]):
    if isinstance(data[0], Category):
        callback = CategoryCallback
        back_button_callback_data = '/start'
    else:
        callback = SubcategoryCallback
        back_button_callback_data = CatalogCallback().pack()
    kb = []
    for i in range(0, len(data), 2):
        layer = [
            InlineKeyboardButton(text=data[i].name, callback_data=callback(id=data[i].id).pack())
        ]
        try:
            layer.append(
                InlineKeyboardButton(text=data[i + 1].name, callback_data=callback(id=data[i + 1].id).pack())
            )
        except IndexError:
            pass
        kb.append(layer)

    if isinstance(data[0], Subcategory):
        kb.append([InlineKeyboardButton(text='« В каталог', callback_data=back_button_callback_data)])
    return InlineKeyboardMarkup(inline_keyboard=kb)


back_to_catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=back_button_style, callback_data=CatalogCallback().pack())
        ]
    ]
)


def back_to_subcategories(category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back_button_style,
                                     callback_data=CategoryCallback(id=category_id).pack())
            ]
        ]
    )


# ================================ KEYBOARDS FOR PRODUCTS ================================ #
def build_products_page(data: Sequence[Product], category_id):
    kb = []
    for i in range(len(data)):
        layer = [
            InlineKeyboardButton(text=f'{data[i].name} • {round_number(data[i].price)}₽',
                                 callback_data=ProductCallback(id=data[i].id).pack())
        ]
        kb.append(layer)
    kb.append(
        [
            InlineKeyboardButton(
                text='« В каталог',
                callback_data=CategoryCallback(id=category_id).pack()
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=kb)


def build_product_panel(product: Product, url, product_name):
    share_text = f"""🔗 Выбранный товар: {product_name}

▼ Ссылка на товар
{url}"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🛒Купить',
                    callback_data=BuyProductCallback(
                        id=product.id,
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(text='🧷Поделиться', copy_text=CopyTextButton(
                    text=share_text
                ))
            ],
            [
                InlineKeyboardButton(text='🎟 Активировать промокод',
                                     callback_data=ActivePromocodeBuyProduct(
                                         id=product.id,
                                     ).pack())
            ],
            [
                InlineKeyboardButton(text=back_button_style,
                                     callback_data=SubcategoryCallback(id=product.subcategory_id).pack())
            ],
        ]
    )


# ================================ KEYBOARDS FOR BUY PRODUCT ================================ #

def back_to_product(product_id, style: Optional[str] = back_button_style):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=style, callback_data=ProductCallback(id=product_id).pack())
            ]
        ]
    )


def back_to_profile(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(text='Профиль ›', callback_data=ProfileCallback().pack())
                            ],
                        ] + back_to_product(product_id).inline_keyboard
    )


def build_buy_product_with_promocode(product_id, promocode):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Перейти к покупке ›',
                                    callback_data=BuyProductCallback(
                                        id=product_id,
                                        promocode=promocode
                                    ).pack()
                                )
                            ],
                        ] + back_to_product(product_id).inline_keyboard
    )


success_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🛍История покупок', callback_data=PurchaseHistoryCallback().pack())
        ]
    ]
)


def select_buy_product_method(product_id: int, amount: float, promocode: Optional[str] = None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🏦 Оплатить с баланса', callback_data='')
            ],
            [
                InlineKeyboardButton(
                    text='🔥 CryptoBot 🔥',
                    callback_data=BuyProductWithPaymentSystem(
                        product_id=product_id,
                        promocode=promocode,
                        amount=amount,
                        system="cryptobot"
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='Картой',
                    callback_data=BuyProductWithPaymentSystem(
                        product_id=product_id,
                        promocode=promocode,
                        amount=amount,
                        system="aaio"
                    ).pack()
                ),
                InlineKeyboardButton(
                    text='Картой/СБП',
                    callback_data=BuyProductWithPaymentSystem(
                        product_id=product_id,
                        promocode=promocode,
                        amount=amount,
                        system="nicepay"
                    ).pack()
                ),

            ],
            [
                InlineKeyboardButton(text=back_button_style, callback_data=ProductCallback(id=product_id).pack())
            ]
        ]
    )
