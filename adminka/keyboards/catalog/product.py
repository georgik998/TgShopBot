from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.callbacks.catalog.product import *

from tg_bot.adminka.keyboards.main import back_to_admin_button
from tg_bot.adminka.keyboards.catalog.main import back_to_catalog_panel_button
from tg_bot.config import back_button_style

from typing import Sequence
from tg_bot.infra.database.models import Product, Category, Subcategory

back_to_product_panel_button = InlineKeyboardButton(text=back_button_style, callback_data=ProductPanelCallback().pack())


def select_category_for_product_manage(categories: Sequence[Category]):
    kb = []
    for category in categories:
        kb.append([
            InlineKeyboardButton(
                text=category.name,
                callback_data=SelectCategoryForProductCallback(
                    category_id=category.id,
                    subcategory_id=None
                ).pack()),
        ])
    kb.append([
        back_to_catalog_panel_button
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def select_subcategory_for_product_manage(subcategories: Sequence[Subcategory]):
    kb = []
    for subcategory in subcategories:
        kb.append([
            InlineKeyboardButton(
                text=subcategory.name,
                callback_data=SelectSubcategoryForProductCallback(
                    subcategory_id=subcategory.id
                ).pack()),
        ])
    kb.append([
        back_to_product_panel_button
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def products_manage(products: Sequence[Product], subcategory_id):
    kb = []
    for product in products:
        kb.append([
            InlineKeyboardButton(
                text=product.name,
                callback_data='snus'
            ),
            InlineKeyboardButton(
                text='❌',
                callback_data=DeleteProductCallback(
                    product_id=product.id,
                    subcategory_id=subcategory_id
                ).pack()),
            InlineKeyboardButton(
                text='✏️',
                callback_data=EditProductCallback(
                    product_id=product.id,
                    subcategory_id=subcategory_id).pack()
            )
        ])
    kb.append([
        InlineKeyboardButton(
            text='➕ Добавить новый',
            callback_data=NewProductCallback(
                subcategory_id=subcategory_id
            ).pack())
    ])
    kb.append([
        InlineKeyboardButton(
            text=back_button_style,
            callback_data=SelectCategoryForProductCallback(
                subcategory_id=subcategory_id).pack()
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def back_to_product_manage(subcategory_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=back_button_style,
                    callback_data=SelectSubcategoryForProductCallback(
                        subcategory_id=subcategory_id
                    ).pack()
                )
            ]
        ]
    )


def confirm_delete_product(product_id, subcategory_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text='Да, я уверен на 100%',
                                    callback_data=ConfirmDeleteProductCallback(
                                        product_id=product_id,
                                        subcategory_id=subcategory_id,
                                        action=True
                                    ).pack()),
                                InlineKeyboardButton(
                                    text='✅ Нет',
                                    callback_data=ConfirmDeleteProductCallback(
                                        product_id=product_id,
                                        subcategory_id=subcategory_id,
                                        action=False
                                    ).pack()),
                            ],
                        ] + back_to_product_manage(subcategory_id).inline_keyboard
    )


def product_edit(product: Product, subcategory_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
                            [
                                InlineKeyboardButton(text=product.name, callback_data='snus')
                            ],
                            [
                                InlineKeyboardButton(text=f'{product.price}₽', callback_data='snus'),
                                InlineKeyboardButton(text=f'{len(product.content)} шт.', callback_data='snus')
                            ],
                            [
                                InlineKeyboardButton(
                                    text='🏷 Изменить название',
                                    callback_data=EditProductItem(
                                        product_id=product.id,
                                        subcategory_id=subcategory_id,
                                        action='name'
                                    ).pack()
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text='🖼 Изменить фото',
                                    callback_data=EditProductItem(
                                        product_id=product.id,
                                        subcategory_id=subcategory_id,
                                        action='photo'
                                    ).pack()
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text='💸 Изменить цену',
                                    callback_data=EditProductItem(
                                        product_id=product.id,
                                        subcategory_id=subcategory_id,
                                        action='price'
                                    ).pack()
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text='✏️ Изменить описание',
                                    callback_data=EditProductItem(
                                        product_id=product.id,
                                        subcategory_id=subcategory_id,
                                        action='description'
                                    ).pack()
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text='💠 Добавить контент',
                                    callback_data=EditProductItem(
                                        product_id=product.id,
                                        subcategory_id=subcategory_id,
                                        action='content'
                                    ).pack()
                                )
                            ],
                        ] + back_to_product_manage(subcategory_id).inline_keyboard
    )


def back_to_product_edit(product_id, subcategory_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=back_button_style,
                    callback_data=EditProductCallback(
                        product_id=product_id,
                        subcategory_id=subcategory_id
                    ).pack()
                )
            ]
        ]
    )
