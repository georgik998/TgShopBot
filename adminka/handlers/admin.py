from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from tg_bot.adminka.callbacks.admin import *
from tg_bot.adminka.callbacks.main import AdminCallback
from tg_bot.adminka.keyboards import admin as kb
from tg_bot.adminka.states.admin import *

from tg_bot.adminka.repositories.user import UserRepo
from tg_bot.infra.database import async_session

from tg_bot.keyboards.main import start_for_admin as kb_start_for_admin, start as kb_start

router = Router()


@router.callback_query(
    AdminCallback.filter(),
    StateFilter(default_state)
)
async def admin_cmd(call: CallbackQuery):
    async with async_session() as session:
        admins = await UserRepo(session).get_admins()
    await call.message.edit_text(
        text='Список админов', reply_markup=kb.build_admins_panel(admins)
    )


@router.callback_query(
    DeleteAdminCallback.filter(),
    StateFilter(
        default_state,
        AdminStates.new
    )
)
async def delete_admin_cmd(call: CallbackQuery, state: FSMContext, callback_data: DeleteAdminCallback, bot: Bot):
    user_id = callback_data.id
    async with async_session() as session:
        await UserRepo(session).set_admin(tg_id=user_id, is_admin=False)
        admins = await UserRepo(session).get_admins()
    try:
        await bot.send_message(
            chat_id=user_id,
            text='😭 У вас забрали админ права',
            reply_markup=kb_start
        )
    except TelegramBadRequest:
        ...
    except TelegramForbiddenError:
        ...
    await call.answer('Обновлено.')
    await call.message.edit_text(
        text='Список админов', reply_markup=kb.build_admins_panel(admins)
    )


@router.callback_query(NewAdminCallback.filter(), StateFilter(default_state))
async def new_admin_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.new)
    await call.message.edit_text(
        'Пришлите id админа для добавления',
        reply_markup=kb.back_to_admin_manage
    )


@router.message(StateFilter(AdminStates.new))
async def new_admin_process_cmd(message: Message, state: FSMContext, bot: Bot):
    try:
        admin_id = int(message.text)
    except ValueError:
        await message.answer(
            'ID админа должно быть целым число, попробуйте снова',
            reply_markup=kb.back_to_admin_manage
        )
        return
    async with async_session() as session:
        is_exist = await UserRepo(session).get_user(admin_id)
        if not is_exist:
            await UserRepo(session).post_user(tg_id=admin_id, father_id=message.from_user.id)
        await UserRepo(session).set_admin(tg_id=admin_id, is_admin=True)

    await state.clear()
    try:
        await bot.send_message(
            chat_id=admin_id,
            text='👁🧠 Вас сделали админом',
            reply_markup=kb_start_for_admin
        )
    except TelegramBadRequest:
        ...
    except TelegramForbiddenError:
        ...
    await message.answer(
        'Новый админ был успено добавлен', reply_markup=kb.back_to_admin_manage
    )
