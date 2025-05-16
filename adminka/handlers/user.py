from aiogram import F, Router, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from tg_bot.adminka.keyboards import user as kb
from tg_bot.adminka.keyboards.main import back_to_admin_kb, UserCallback
from tg_bot.adminka.callbacks.user import *
from tg_bot.adminka.states.user import UserStates
from tg_bot.utils import round_number

from tg_bot.adminka.repositories.user import UserRepo, UserPurchasesRepo
from tg_bot.infra.database import async_session

from tg_bot.adminka.utils import parse_text

router = Router()


def build_text(user, purchases_count, purchases_amount):
    return f"""<blockquote>
🦣 <del>Мамонт</del> Юзер: <code>{user.tg_id}</code>

💸 Общий баланс: <code>{round_number(user.balance)}₽</code>
🏛 Баланс: <code>{round_number(user.balance - user.referral_balance)}₽</code>
👥 Реферальный баланс: <code>{round_number(user.referral_balance)}₽</code>

🛍 Покупок: {purchases_count}
💸 Сумма покупок: {round_number(purchases_amount)}

⏳ Дата регистрации: {user.registration_date.strftime("%d.%m.%Y")}
⛔️ Бан: {"✅" if user.is_blocked else "❌"}
💠 Админ: {"✅" if user.is_admin else "❌"}
</blockquote>"""


@router.callback_query(UserCallback.filter(),
                       StateFilter(default_state))
async def user_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.id)
    await call.message.edit_text(
        'Пришлите id юзера чтобы найти его',
        reply_markup=back_to_admin_kb
    )


@router.message(StateFilter(UserStates.id))
async def user_panel_cmd(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer(
            'ID должно быть целым числом, попробуйте еще раз',
            reply_markup=back_to_admin_kb
        )
        return
    async with async_session() as session:
        user = await UserRepo(session).get_user(user_id)
        purchases_count = await UserPurchasesRepo(session).get_purchases_count(user_id)
        purchases_amount = await UserPurchasesRepo(session).get_purchases_amount(user_id)
    if not user:
        await message.answer(
            'Юзера с таким id не существует, попробуйте еще раз',
            reply_markup=back_to_admin_kb
        )
        return
    await state.clear()
    await message.answer(
        text=build_text(user, purchases_count, purchases_amount),
        reply_markup=kb.user_manage_panel(user_id, user.is_blocked)
    )


@router.callback_query(BackToUserPanel.filter(),
                       StateFilter(default_state,UserStates.give_balance, UserStates.claim_balance, UserStates.send_sms,
                                   UserStates.send_sms_confirm))
async def back_user_panel_cmd(call: CallbackQuery, callback_data: BackToUserPanel, state: FSMContext):
    user_id = callback_data.id
    async with async_session() as session:
        user = await UserRepo(session).get_user(user_id)
        purchases_count = await UserPurchasesRepo(session).get_purchases_count(user_id)
        purchases_amount = await UserPurchasesRepo(session).get_purchases_amount(user_id)
    await state.clear()
    await call.message.edit_text(
        text=build_text(user, purchases_count, purchases_amount),
        reply_markup=kb.user_manage_panel(user_id, user.is_blocked)
    )


@router.callback_query(BanUserCallbackData.filter(), StateFilter(default_state))
async def ban_user_cmd(call: CallbackQuery, callback_data: BanUserCallbackData):
    user_id = callback_data.id
    async with async_session() as session:
        await UserRepo(session).ban_user(user_id)
        user = await UserRepo(session).get_user(user_id)
        purchases_count = await UserPurchasesRepo(session).get_purchases_count(user_id)
        purchases_amount = await UserPurchasesRepo(session).get_purchases_amount(user_id)
    await call.answer('Забанен.')
    await call.message.edit_text(
        text=build_text(user, purchases_count, purchases_amount),
        reply_markup=kb.user_manage_panel(user_id, user.is_blocked)
    )


@router.callback_query(UnbanUserCallbackData.filter(), StateFilter(default_state))
async def ban_user_cmd(call: CallbackQuery, callback_data: UnbanUserCallbackData):
    user_id = callback_data.id
    async with async_session() as session:
        await UserRepo(session).unban_user(user_id)
        user = await UserRepo(session).get_user(user_id)
        purchases_count = await UserPurchasesRepo(session).get_purchases_count(user_id)
        purchases_amount = await UserPurchasesRepo(session).get_purchases_amount(user_id)
    await call.answer('Разбанен.')
    await call.message.edit_text(
        text=build_text(user, purchases_count, purchases_amount),
        reply_markup=kb.user_manage_panel(user_id, user.is_blocked)
    )


@router.callback_query(GiveBalanceUserCallbackData.filter(), StateFilter(default_state))
async def give_balance_cmd(call: CallbackQuery, callback_data: GiveBalanceUserCallbackData, state: FSMContext):
    user_id = callback_data.id
    await state.set_state(UserStates.give_balance)
    await state.update_data({'user_id': user_id})
    await call.message.edit_text(
        'Напиши сколько баланса вы хотите добавить юзеру',
        reply_markup=kb.back_to_user_panel(user_id)
    )


@router.message(StateFilter(UserStates.give_balance))
async def give_balance_process(message: Message, state: FSMContext):
    user_id = await state.get_value('user_id')
    try:
        balance_delta = float(message.text)
    except ValueError:
        await message.answer(
            'Баланс должен быть целым числом, попробуйте снова',
            reply_markup=kb.back_to_user_panel(user_id)
        )
        return
    async with async_session() as session:
        await UserRepo(session).update_balance(user_id, balance_delta)
    await message.answer(
        'Баланс юзера был пополнен',
        reply_markup=kb.back_to_user_panel(user_id)
    )


@router.callback_query(ClaimBalanceUserCallbackData.filter(), StateFilter(default_state))
async def claim_balance_cmd(call: CallbackQuery, callback_data: GiveBalanceUserCallbackData, state: FSMContext):
    user_id = callback_data.id
    await state.set_state(UserStates.claim_balance)
    await state.update_data({'user_id': user_id})
    await call.message.edit_text(
        'Напиши сколько баланса вы хотите забрать у  юзера',
        reply_markup=kb.back_to_user_panel(user_id)
    )


@router.message(StateFilter(UserStates.claim_balance))
async def claim_balance_process(message: Message, state: FSMContext):
    user_id = await state.get_value('user_id')
    try:
        balance_delta = float(message.text)
    except ValueError:
        await message.answer(
            'Баланс должен быть целым числом, попробуйте снова',
            reply_markup=kb.back_to_user_panel(user_id)
        )
        return
    async with async_session() as session:
        await UserRepo(session).update_balance(user_id, -balance_delta)
    await message.answer(
        'Баланс юзера был понижен',
        reply_markup=kb.back_to_user_panel(user_id)
    )


@router.callback_query(SendMessageUserCallbackData.filter(), StateFilter(default_state))
async def send_sms_cmd(callback: CallbackQuery, callback_data: SendMessageUserCallbackData, state: FSMContext):
    user_id = callback_data.id
    await state.update_data({'user_id': user_id})
    await state.set_state(UserStates.send_sms)
    await callback.message.edit_text(
        'Пришлите сообщение которое хотите отправить юзеру',
        reply_markup=kb.back_to_user_panel(user_id)
    )


@router.message(StateFilter(UserStates.send_sms))
async def send_sms_confirm_cmd(message: Message, state: FSMContext, bot: Bot):
    await state.set_state(UserStates.send_sms_confirm)
    await state.update_data({'message_id': message.message_id})
    await bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer(
        'Проверьте сообщение выше, если все устраивает потвердите отправку',
        reply_markup=kb.confirm_send_sms(user_id=await state.get_value('user_id'))
    )


@router.callback_query(SendMessageUserConfirmCallbackData.filter(), StateFilter(UserStates.send_sms_confirm))
async def confirm_send_sms_cmd(call: CallbackQuery, state: FSMContext,
                               callback_data: SendMessageUserConfirmCallbackData,bot:Bot):
    action = callback_data.action
    data = await state.get_data()
    message_id, user_id = data['message_id'], data['user_id']
    await state.clear()
    if not action:
        await call.message.edit_text(
            'Отменено',
            reply_markup=kb.back_to_user_panel(user_id)
        )
    else:
        await call.answer('Отправляем...')
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=call.message.chat.id,
            message_id=message_id
        )
        await call.message.edit_text(
            'Успешно отправлено!',
            reply_markup=kb.back_to_user_panel(user_id)
        )

