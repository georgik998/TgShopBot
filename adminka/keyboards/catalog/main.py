from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.adminka.callbacks.catalog.product import ProductPanelCallback
from tg_bot.adminka.callbacks.catalog.category import CategoryPanelCallback
from tg_bot.adminka.callbacks.catalog.subcategory import SubcategoryPanelCallback
from tg_bot.adminka.callbacks.main import CatalogCallback

from tg_bot.config import back_button_style

from tg_bot.adminka.keyboards.main import back_to_admin_button

catalog_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📦 Управление категориями', callback_data=CategoryPanelCallback().pack())
        ],
        [
            InlineKeyboardButton(text='📚 Управление подкатегориями', callback_data=SubcategoryPanelCallback().pack())
        ],
        [
            InlineKeyboardButton(text='🛍 Управление продуктами', callback_data=ProductPanelCallback().pack())
        ],
        [
            back_to_admin_button
        ]
    ]
)

back_to_catalog_panel_button = InlineKeyboardButton(text=back_button_style, callback_data=CatalogCallback().pack())
back_to_product_panel_button = InlineKeyboardButton(text=back_button_style, callback_data=ProductPanelCallback().pack())
