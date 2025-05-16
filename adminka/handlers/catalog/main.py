from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.adminka.callbacks.main import CatalogCallback
from tg_bot.adminka.keyboards.catalog.main import catalog_panel

router = Router()


@router.callback_query(CatalogCallback.filter(), StateFilter(default_state))
async def catalog_cmd(call: CallbackQuery):
    await call.message.edit_text(
        'Выберите действие',
        reply_markup=catalog_panel
    )
