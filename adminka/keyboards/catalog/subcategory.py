from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.callbacks.catalog.subcategory import *
from tg_bot.adminka.keyboards.catalog.main import back_to_catalog_panel_button

from tg_bot.adminka.config import back_button_style

from tg_bot.infra.database.models import Subcategory, Category
from typing import Sequence


def build_category_select_panel(categories: Sequence[Category]):
    kb = []
    for category in categories:
        kb.append([
            InlineKeyboardButton(text=category.name,
                                 callback_data=SelectCategoryForSubcategoryEditPanelCallback(id=category.id).pack()),
        ])
    kb.append([
        back_to_catalog_panel_button
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def build_category_select_fot_new_subcategory(categories: Sequence[Category]):
    kb = []
    for category in categories:
        kb.append([
            InlineKeyboardButton(text=category.name,
                                 callback_data=SelectCategoryForNewSubcategoryCallback(id=category.id).pack()),
        ])
    kb.append([
        back_to_catalog_panel_button
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def build_subcategory_manage_panel(subcategories: Sequence[Subcategory], category_id):
    kb = []
    for subcategory in subcategories:
        kb.append([
            InlineKeyboardButton(text=subcategory.name, callback_data='snus'),
            InlineKeyboardButton(text='❌', callback_data=DeleteSubcategoryCallback(id=subcategory.id,
                                                                                   category_id=category_id).pack()),
            InlineKeyboardButton(text='✏️', callback_data=EditSubcategoryNameCallback(id=subcategory.id,
                                                                                      category_id=category_id).pack()),
            InlineKeyboardButton(text='📖️', callback_data=EditSubcategoryDescriptionCallback(
                id=subcategory.id,
                category_id=category_id
            ).pack()),
        ])
    kb.append([InlineKeyboardButton(text='➕ Добавить новую',
                                    callback_data=NewSubcategoryCallback(category_id=category_id).pack())])
    kb.append([InlineKeyboardButton(text=back_button_style, callback_data=SubcategoryPanelCallback().pack())])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def confirm_delete_subcategory(subcategory_id, category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да, я уверен',
                                     callback_data=ConfirmDeleteSubcategoryCallback(id=subcategory_id,
                                                                                    action=True,
                                                                                    category_id=category_id).pack()),
                InlineKeyboardButton(text='✅Отменить',
                                     callback_data=ConfirmDeleteSubcategoryCallback(id=subcategory_id,
                                                                                    action=False,
                                                                                    category_id=category_id).pack()),
            ],
            [
                InlineKeyboardButton(text=back_button_style,
                                     callback_data=SelectCategoryForSubcategoryEditPanelCallback(id=category_id).pack())
            ]
        ]
    )


def back_to_subcategory_edit_panel(category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=back_button_style,
                    callback_data=SelectCategoryForSubcategoryEditPanelCallback(
                        id=category_id
                    ).pack())
            ]
        ]
    )
