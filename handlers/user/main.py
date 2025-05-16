from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import default_state
from aiogram.exceptions import TelegramBadRequest

from datetime import timedelta

from tg_bot.states.payment import PaymentStates
from tg_bot.keyboards import main as kb
from tg_bot.keyboards.catalog import build_product_panel
from tg_bot.utils import *
from tg_bot.callbacks.main import InfoCallback, FaqCallback, FaqAnswerCallback, CheckSubscribe

from tg_bot.repositories.user import UserRepo
from tg_bot.repositories.content import TextRepo, ContactsRepo, FaqRepo, SubscribeChannelRepo, BannerRepo, \
    NotifyChannelRepo
from tg_bot.services.tg_admin_log import TgAdminLogService
from tg_bot.repositories.catalog import ProductRepo
from tg_bot.infra.database import async_session

from tg_bot.locales import texts

router = Router()


# ================================  HANDLER FOR START BOT WITH SHARE PRODUCT LINK ================================ #
@router.message(CommandStart(deep_link=True))
async def start_bot_with_share_product_cmd(message: Message, state: FSMContext, command: CommandObject, bot: Bot):
    father_id, product_id = parse_link(command.args)
    async with async_session() as session:
        is_admin = await UserRepo(session).is_admin(message.from_user.id)
        start_text = await TextRepo(session).get_text('start')
        start_banner = await BannerRepo(session).get('start')
        if product_id != 0 and product_id is not None:
            product = await ProductRepo(session).get_product(product_id)
    await state.clear()
    if product_id != 0 and product_id is not None:
        await message.answer_photo(
            photo=product.photo,
            caption=product.description,
            reply_markup=build_product_panel(product, url=create_product_link(product_id, message.from_user.id),
                                             product_name=product.name)
        )
    else:
        await message.answer_photo(
            photo=start_banner,
            caption=start_text,
            reply_markup=kb.start if not is_admin else kb.start_for_admin
        )


# ================================  HANDLER FOR START ================================ #
@router.message(CommandStart(deep_link=False))
async def start_cmd(message: Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        is_new_user = await UserRepo(session).post_user(message.from_user.id)
        is_admin = await UserRepo(session).is_admin(message.from_user.id)
        start_text = await TextRepo(session).get_text('start')
        start_banner = await BannerRepo(session).get('start')
        if is_new_user:
            notify_channels = await NotifyChannelRepo(session).get_channels()
    if is_new_user:
        await TgAdminLogService(bot=bot, user_tg_id=message.from_user.id, username=message.from_user.username,
                                channels=notify_channels).send_new_user(
            ref_link='отсутствует')
    await state.clear()
    await message.answer_photo(
        photo=start_banner,
        caption=start_text,
        reply_markup=kb.start if not is_admin else kb.start_for_admin
    )


@router.callback_query(F.data == '/start', StateFilter(default_state, PaymentStates.amount))
async def start_callback_cmd(call: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        is_admin = await UserRepo(session).is_admin(call.from_user.id)
        start_text = await TextRepo(session).get_text('start')
        start_banner = await BannerRepo(session).get('start')
    await state.clear()
    await call.message.edit_media(
        media=InputMediaPhoto(
            media=start_banner,
            caption=start_text
        ),
        # reply_markup=kb.start if not is_admin else kb.start_for_admin
    )


# ======================== INFO: handlers for information ========================

@router.message(F.text == 'ℹ️ Информация')
async def info_cmd(message: Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        info_text = await TextRepo(session).get_text('info')
        info_banner = await BannerRepo(session).get('info')
        contacts = await ContactsRepo(session).get_contacts()
    await state.clear()
    sms = await message.answer('📚')
    # await sleep(delay_before_delete_emoji)
    # await bot.delete_message(
    #     chat_id=message.from_user.id,
    #     message_id=sms.message_id
    # )
    await message.answer_photo(
        photo=info_banner,
        caption=info_text,
        reply_markup=kb.info(
            review_url=contacts.review,
            owner_url=contacts.owner,
            news_url=contacts.news,
            support_url=contacts.support
        )
    )


@router.callback_query(InfoCallback.filter(), StateFilter(default_state))
async def info_cmd(call: CallbackQuery):
    async with async_session() as session:
        info_text = await TextRepo(session).get_text('info')
        contacts = await ContactsRepo(session).get_contacts()
    await call.message.edit_caption(
        caption=info_text,
        reply_markup=kb.info(
            review_url=contacts.review,
            owner_url=contacts.owner,
            news_url=contacts.news,
            support_url=contacts.support
        )
    )


# ======================== FAQ: handlers for faq questions ========================

@router.callback_query(FaqCallback.filter(), StateFilter(default_state))
async def faq_cmd(call: CallbackQuery):
    async with async_session() as session:
        faq_info = await FaqRepo(session).get_faq()
        faq_text = await TextRepo(session).get_text('faq')
    await call.message.edit_caption(
        caption=faq_text,
        reply_markup=kb.build_faq(faq_info)
    )


@router.callback_query(FaqAnswerCallback.filter(), StateFilter(default_state))
async def faq_answer_cmd(call: CallbackQuery, callback_data: FaqAnswerCallback):
    faq_question_id = callback_data.id
    async with async_session() as session:
        answer = await FaqRepo(session).get_answer(faq_question_id)
    await call.message.edit_caption(
        caption=answer,
        reply_markup=kb.back_to_faq
    )


# ======================== CHANNEL SUBSCRIBE CHECK ========================

@router.callback_query(CheckSubscribe.filter(), StateFilter(default_state))
async def check_subscribe_cmd(call: CallbackQuery, bot: Bot):
    async with async_session() as session:
        channels = await SubscribeChannelRepo(session).get_channels()
    no_subscribe_channels_urls = await check_subscribe(channels=channels, user_id=call.from_user.id, bot=bot)
    if no_subscribe_channels_urls:
        try:
            await call.message.edit_text(
                text='Вы не дописаны на нужные каналы, чтобы пользоваться ботом, подпишитесь на них',
                reply_markup=kb.channel_to_subscribe(no_subscribe_channels_urls)
            )
        except TelegramBadRequest:
            await call.answer('❌Вы не подписаны на каналы')
        return
    await call.message.edit_text(
        'Поздравляем! Можете пользоваться ботом!'
    )


@router.callback_query(F.data == 'cancel')
async def cancel_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer('Отменено.')
    await call.message.delete()


# ======================== OTHER HANDLERS ========================
from tg_bot.keyboards.payment import payment_amounts


@router.message(F.text == '➕ Пополнить баланс')
async def payment_cmd(message: Message, state: FSMContext, bot: Bot, ):
    async with async_session() as session:
        payment_text = await TextRepo(session).get_text('payment')
        payment_banner = await BannerRepo(session).get('payment')
    await state.set_state(PaymentStates.amount)
    sms = await message.answer('💸')
    # await sleep(delay_before_delete_emoji)
    # await bot.delete_message(
    #     chat_id=message.from_user.id,
    #     message_id=sms.message_id
    # )
    await message.answer_photo(
        photo=payment_banner,
        caption=payment_text,
        reply_markup=payment_amounts
    )


from tg_bot.repositories.user import UserPurchasesRepo
from tg_bot.keyboards.profile import build_profile


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
        ),
        reply_markup=build_profile()
    )


from tg_bot.repositories.catalog import CategoryRepo
from tg_bot.keyboards.catalog import build_catalog_page


@router.message(F.text == '🗂 Каталог товаров')
async def catalog_cmd(message: Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        categories = await CategoryRepo(session).get_categories()
        catalog_banner = await BannerRepo(session).get('catalog')
    if not categories:
        await message.answer_photo(
            photo=catalog_banner,
            caption='Ой-ой! Пока товара нет в наличии, попробуйте позже'
        )
        return
    await state.clear()
    sms = await message.answer('🛒')
    # await sleep(delay_before_delete_emoji)
    # await bot.delete_message(
    #     chat_id=message.from_user.id,
    #     message_id=sms.message_id
    # )
    await message.answer_photo(
        photo=catalog_banner,
        caption=texts['ru']['catalog']['select_category'],
        reply_markup=build_catalog_page(categories)
    )


@router.callback_query(F.data == 'snus')
async def snus_cmd(call: CallbackQuery):
    await call.answer('Code By George🐠')
