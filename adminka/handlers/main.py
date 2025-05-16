from aiogram import F, Router, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.filters import or_f
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from tg_bot.adminka.keyboards import main as kb
from tg_bot.adminka.callbacks.main import AdminPanelCallback

from tg_bot.adminka.states.user import UserStates
from tg_bot.adminka.states.spam import SpamStates

from tg_bot.adminka.repositories.user import UserRepo
from tg_bot.infra.database import async_session

router = Router()


@router.message(or_f(F.text == '/admin', F.text == '💠 Админ панель'), StateFilter(default_state))
async def admin_cmd(message: Message):
    await message.answer(
        text=f'💠 <i>{message.from_user.first_name if message.from_user.first_name else "Админ"}</i>, добро пожаловать в админ панель!',
        reply_markup=kb.admin
    )


@router.callback_query(
    AdminPanelCallback.filter(),
    StateFilter(
        default_state,
        UserStates.id,
        SpamStates.sms
    )
)
async def admin_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text=f'💠 <i>{call.from_user.first_name if call.from_user.first_name else "Админ"}</i>, добро пожаловать в админ панель!',
        reply_markup=kb.admin
    )


@router.my_chat_member()
async def on_my_chat_member(update: ChatMemberUpdated, bot: Bot):
    if update.new_chat_member.status in ["member", "administrator"]:
        chat_id = update.chat.id
        async with async_session() as session:
            admins = await UserRepo(session).get_admins()
        for admin in admins:
            await bot.send_message(admin, f"Привет! ID этого чата: <code>{chat_id}</code>")
