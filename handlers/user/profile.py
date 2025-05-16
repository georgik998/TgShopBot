from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, BufferedInputFile, InputMediaDocument
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from datetime import timedelta

from tg_bot.keyboards import profile as kb
from tg_bot.callbacks.main import ProfileCallback
from tg_bot.callbacks.profile import *

from tg_bot.repositories.user import UserRepo, UserPurchasesRepo, UserPromocodeRepo
from tg_bot.repositories.content import PromocodeRepo, BannerRepo, NotifyChannelRepo
from tg_bot.services.tg_admin_log import TgAdminLogService
from tg_bot.infra.database import async_session

from tg_bot.utils import *
from tg_bot.config import bot_settings

from tg_bot.locales import texts

from tg_bot.states.profile import PromocodeStates
from io import BytesIO

router = Router()


# ======================== PROFILE: handlers for profile ========================
@router.message(F.text == '🪪 Мой профиль', )
async def profile_cmd(message: Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        user = await UserRepo(session).get_user(message.from_user.id)
        purchases_count = await UserPurchasesRepo(session).get_purchases_count(message.from_user.id)
        purchases_amount = await UserPurchasesRepo(session).get_purchases_amount(message.from_user.id)
        profile_banner = await BannerRepo(session).get('profile')
    await state.clear()
    sms = await message.answer('🪪')
    await message.answer_photo(
        photo=profile_banner,
        caption=texts['ru']['profile']['main'](
            user.tg_id,
            user.registration_date + timedelta(hours=3),
            round_number(user.balance),
            round_number(user.referral_balance),
            purchases_count,
            round_number(purchases_amount)
        ), reply_markup=kb.build_profile()
    )


@router.callback_query(ProfileCallback.filter(), StateFilter(default_state, PromocodeStates.promocode))
async def profile_cmd(call: CallbackQuery, state: FSMContext, bot: Bot):
    async with async_session() as session:
        user = await UserRepo(session).get_user(call.from_user.id)
        purchases_count = await  UserPurchasesRepo(session).get_purchases_count(call.from_user.id)
        purchases_amount = await  UserPurchasesRepo(session).get_purchases_amount(call.from_user.id)
        profile_banner = await BannerRepo(session).get('profile')
        main_message_id = await state.get_value('main_message_id')
    await state.clear()
    text = texts['ru']['profile']['main'](
        user.tg_id,
        user.registration_date + timedelta(hours=3),
        round_number(user.balance),
        round_number(user.referral_balance),
        purchases_count,
        round_number(purchases_amount)
    )
    if call.message.photo:
        message = await call.message.edit_caption(
            caption=text, reply_markup=kb.build_profile()
        )
    else:
        message = await call.message.edit_media(
            media=InputMediaPhoto(
                media=profile_banner,
                caption=text
            ),
            reply_markup=kb.build_profile()
        )
    if main_message_id:
        await bot.delete_messages(
            chat_id=call.from_user.id,
            message_ids=[message_id for message_id in range(main_message_id, message.message_id)]
        )


# ======================== PURCHASES: handlers for purchases history ========================
@router.callback_query(PurchaseHistoryCallback.filter(), StateFilter(default_state))
async def purchases_history_cmd(call: CallbackQuery, callback_data: PurchaseHistoryCallback):
    async with async_session() as session:
        purchases = await UserPurchasesRepo(session).get_purchases(call.from_user.id)
        if purchases:
            purchases = purchases[::-1]
        if call.message.document:  # если вернулись после успешной покупки
            profile_banner = await BannerRepo(session).get('profile')
    if not purchases:
        await call.answer('💢 У вас нет ни одной покупки', show_alert=True)
        return
    page = callback_data.page
    if call.message.document:  # если вернулись после успешной покупки
        await call.message.edit_media(
            media=InputMediaPhoto(
                media=profile_banner,
                caption='▼ Выберите одну из покупок для просмотра информации:',
            ),
            reply_markup=kb.build_purchases(purchases, page)
        )
    else:
        await call.message.edit_caption(
            caption='▼ Выберите одну из покупок для просмотра информации:',
            reply_markup=kb.build_purchases(purchases, page)
        )


@router.callback_query(PurchaseCallback.filter(), StateFilter(default_state))
async def purchase_history_purchase_cmd(call: CallbackQuery, callback_data: PurchaseCallback):
    purchase_id = callback_data.id
    page = callback_data.page

    async with async_session() as session:

        purchase = await UserPurchasesRepo(session).get_purchase(purchase_id)
        if not call.message.photo:
            profile_banner = await BannerRepo(session).get('profile')

    if call.message.photo:
        await call.message.edit_caption(
            caption=texts['ru']['profile']["my_purchase"](purchase_id, purchase.name, round_number(purchase.amount)),
            reply_markup=kb.purchase_view(page, purchase_id)
        )
    else:
        await call.message.edit_media(
            media=InputMediaPhoto(
                media=profile_banner,
                caption=texts['ru']['profile']["my_purchase"](purchase_id, purchase.name,
                                                              round_number(purchase.amount)),
            ),
            reply_markup=kb.purchase_view(page, purchase_id)
        )


@router.callback_query(GetPurchaseCallback.filter(), StateFilter(default_state))
async def get_purchase_history_product_cmd(call: CallbackQuery, callback_data: CallbackData):
    purchase_id = callback_data.id
    page = callback_data.page

    async with async_session() as session:
        purchase = await UserPurchasesRepo(session).get_purchase(purchase_id)

    await call.message.edit_media(
        media=InputMediaDocument(
            media=BufferedInputFile(
                BytesIO(purchase.content.encode("utf-8")).read(),
                filename=f"{purchase.name}.txt"
            ),
            caption='Вот ваш товар! Поздравляем',
        ),
        reply_markup=kb.get_purchase(purchase_id, page)
    )


# ======================== PROMOCODE ========================
@router.callback_query(ActivatePromocodeCallback.filter(), StateFilter(default_state))
async def payment_active_promo(call: CallbackQuery, state: FSMContext):
    await state.set_state(PromocodeStates.promocode)
    message = await call.message.edit_caption(
        caption=texts['ru']['catalog']['activate_promo'],
        reply_markup=kb.back_to_profile
    )
    await state.update_data({
        'main_message_id': message.message_id
    })


@router.message(StateFilter(PromocodeStates.promocode))
async def payment_active_promo_validate_cmd(message: Message, state: FSMContext, bot: Bot):
    promocode = message.text

    async with async_session() as session:
        promocode = await PromocodeRepo(session).get_promocode_by_name(promocode)
        if promocode is not None and promocode.type.value not in ['discount_percent', 'discount_fix']:
            is_used = await UserPromocodeRepo(session).check_promo(message.from_user.id, promocode.name)
            if not is_used:
                await UserPromocodeRepo(session).add_promo(message.from_user.id, promocode.name)
                await UserRepo(session).update_balance(message.from_user.id, promocode.content)
                await PromocodeRepo(session).post_activation(promocode.name)
                channels = await NotifyChannelRepo(session).get_channels()
    if promocode is None:
        text = texts['ru']['profile']['not_found_promo']
    elif promocode.type.value in ['discount_percent', 'discount_fix']:
        await message.answer('❌')
        await message.answer(
            text=texts['ru']['profile']['promo_error_type'],
            reply_markup=kb.error_promo_type
        )
        return
    elif is_used:
        text = 'Вы уже использовали данный промокод ранее, попробуйте другой'
    else:
        text = texts['ru']['profile']['success_promo'](round_number(promocode.content))
        await TgAdminLogService(
            bot, message.from_user.id, message.from_user.username, channels
        ).send_promocode(promocode=promocode.name, promocode_type=promocode.type)
        await state.clear()
        await message.answer(
            text=text,
            reply_markup=kb.back_to_profile
        )
        return
    await message.answer(
        text=text,
        reply_markup=kb.build_back_to_profile(style='⛌ Отменить ввод ')
    )


@router.callback_query(ReferralSystemCallback.filter(), StateFilter(default_state))
async def referral_system_cmd(call: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        referral_balance = await UserRepo(session).get_referral_balance(call.from_user.id)
        total_ref = await UserRepo(session).count_referrals(father_id=call.from_user.id)
    ref_url = f"{bot_settings.BOT_URL}?start={call.from_user.id}"
    await call.message.edit_caption(
        caption=texts['ru']['profile']["ref_system_description"](referral_balance, total_ref, ref_url),
        reply_markup=kb.ref_system_panel(ref_url)
    )


# ======================== REF SYSTEM ========================
@router.callback_query(WithdrawReferralBalanceCallback.filter(), StateFilter(default_state))
async def withdrawal_referral_system_cmd(call: CallbackQuery):
    async with async_session() as session:
        referral_balance = await UserRepo(session).get_referral_balance(call.from_user.id)
        total_ref = await UserRepo(session).count_referrals(father_id=call.from_user.id)
        if referral_balance != 0:
            await UserRepo(session).update_referral_balance(call.from_user.id, -referral_balance)
            await UserRepo(session).update_balance(call.from_user.id, referral_balance)
    if referral_balance == 0:
        await call.answer('❌ Баланс слишком маленький для вывода')
        return
    await call.answer('✅ Средства отправлены на основной баланс')
    ref_url = f"{bot_settings.BOT_URL}?start={call.from_user.id}"
    await call.message.edit_caption(
        caption=texts['ru']['profile']["ref_system_description"](0, total_ref, ref_url),
        reply_markup=kb.ref_system_panel(ref_url)
    )
