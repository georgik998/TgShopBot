from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, BufferedInputFile
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import default_state

from io import BytesIO

from tg_bot.keyboards import catalog as kb
from tg_bot.callbacks.main import CatalogCallback
from tg_bot.callbacks.catalog import *

from tg_bot.repositories.catalog import CategoryRepo, SubcategoryRepo, ProductRepo
from tg_bot.repositories.content import PromocodeRepo, BannerRepo, NotifyChannelRepo
from tg_bot.services.tg_admin_log import TgAdminLogService
from tg_bot.repositories.user import UserRepo, UserPurchasesRepo, UserPromocodeRepo
from tg_bot.infra.database import async_session
from tg_bot.utils import *

from tg_bot.infra.log import logger

from tg_bot.states.catalog import BuyProductStates
from tg_bot.states.profile import PromocodeStates

from tg_bot.locales import texts

router = Router()


@router.message(F.text == '🗂 Каталог товаров')
async def catalog_cmd(message: Message, state: FSMContext, bot: Bot):
    async with async_session() as session:
        categories = await CategoryRepo(session).get_categories()
        catalog_banner = await BannerRepo(session).get('catalog')
    if not categories:
        await message.answer_photo(
            photo=catalog_banner,
            caption=texts['ru']['catalog']['not_found_product']
        )
        return
    await state.clear()
    await message.answer('🛒')
    await message.answer_photo(
        photo=catalog_banner,
        caption=texts['ru']['catalog']['select_category'],
        reply_markup=kb.build_catalog_page(categories)
    )


@router.callback_query(CatalogCallback.filter(), StateFilter(default_state, PromocodeStates.promocode))
async def catalog_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    async with async_session() as session:
        categories = await CategoryRepo(session).get_categories()
        if not call.message.photo:
            catalog_banner = await BannerRepo(session).get('catalog')
    if not categories:
        await call.message.edit_caption(
            caption=texts['ru']['catalog']['not_found_product']
        )
        return
    if call.message.photo:
        await call.message.edit_caption(
            caption=texts['ru']['catalog']['select_category'],
            reply_markup=kb.build_catalog_page(categories)
        )
    else:  # если пришли после пополнения баланса
        await call.message.edit_media(
            media=InputMediaPhoto(
                media=catalog_banner, caption=texts['ru']['catalog']['select_category'],
            ), reply_markup=kb.build_catalog_page(categories)
        )


@router.callback_query(CategoryCallback.filter(), StateFilter(default_state))
async def subcategory_select_cmd(call: CallbackQuery, callback_data: CategoryCallback):
    category_id = callback_data.id
    async with async_session() as session:
        category = await CategoryRepo(session).get(category_id)
        subcategories = await SubcategoryRepo(session).get_subcategories_by_category_id(category_id)
    if not subcategories:
        await call.message.edit_caption(
            caption=texts['ru']['catalog']['not_found_product'],
            reply_markup=kb.back_to_catalog
        )
        return
    await call.message.edit_caption(
        caption=f"""<b>{category.name}</b>

{category.description}""",
        reply_markup=kb.build_catalog_page(subcategories)
    )


@router.callback_query(SubcategoryCallback.filter(), StateFilter(default_state))
async def product_select_cmd(call: CallbackQuery, callback_data: SubcategoryCallback, bot: Bot):
    subcategory_id = callback_data.id
    async with async_session() as session:
        products = await ProductRepo(session).get_products_by_subcategory_id(subcategory_id)
        category_id = await SubcategoryRepo(session).get_category_id_by_subcategory_id(subcategory_id)
        if products:
            category = await CategoryRepo(session).get(
                await SubcategoryRepo(session).get_category_id_by_subcategory_id(subcategory_id)
            )
            subcategory = await SubcategoryRepo(session).get(subcategory_id)
            catalog_banner = await BannerRepo(session).get('catalog')

    if not products:
        await call.message.edit_caption(
            caption=texts['ru']['catalog']['not_found_product'],
            reply_markup=kb.back_to_subcategories(category_id)
        )
        return
    await call.message.edit_media(
        media=InputMediaPhoto(
            caption=f"""<b>{category.name}</b> › <b>{subcategory.name}</b>

{subcategory.description}""",
            media=catalog_banner
        ),
        reply_markup=kb.build_products_page(products, category_id)
    )


# ================================ PRODUCT HANDLERS: buy product, share product ================================ #

@router.callback_query(ProductCallback.filter(), StateFilter(default_state, BuyProductStates.promocode))
async def product_panel_cmd(call: CallbackQuery, callback_data: ProductCallback, state: FSMContext, bot: Bot):
    product_id = callback_data.id
    async with async_session() as session:
        product = await ProductRepo(session).get_product(product_id)
    main_message_id = await state.get_value('main_message_id')
    await state.clear()
    message = await call.message.edit_media(
        media=InputMediaPhoto(
            media=product.photo,
            caption=texts['ru']['catalog']['product'](product.name, product.price, product.description)
        ),
        reply_markup=kb.build_product_panel(
            product,
            url=create_product_link(product_id, call.from_user.id),
            product_name=product.name
        )
    )
    if main_message_id:
        await bot.delete_messages(
            chat_id=call.from_user.id,
            message_ids=[message_id for message_id in range(main_message_id, message.message_id)]
        )


@router.callback_query(ActivePromocodeBuyProduct.filter(), StateFilter(default_state))
async def buy_product_active_promocode_cmd(call: CallbackQuery, callback_data: ActivePromocodeBuyProduct,
                                           state: FSMContext, bot: Bot):
    product_id = callback_data.id
    await state.update_data({
        'product_id': product_id,

    })
    await state.set_state(BuyProductStates.promocode)
    await call.message.delete()
    message = await bot.send_message(
        chat_id=call.from_user.id,
        text=texts['ru']['catalog']['activate_promo'],
        reply_markup=kb.back_to_product(product_id)
    )
    await state.update_data({
        'main_message_id': message.message_id  # PaymentCallback(),ProductCallback()
    })


@router.message(StateFilter(BuyProductStates.promocode))
async def buy_product_active_promocode_validate_cmd(message: Message, state: FSMContext):
    product_id = await state.get_value('product_id')
    promocode = message.text

    async with async_session() as session:
        promocode = await PromocodeRepo(session).get_promocode_by_name(promocode)
        if promocode:
            product = await ProductRepo(session).get_product(product_id)
            product_price = product.price
            is_used = await UserPromocodeRepo(session).check_promo(message.from_user.id, promocode.name)

    if promocode is None:
        await message.answer(
            text=texts['ru']['catalog']['not_found_promo'],
            reply_markup=kb.back_to_product(product_id, style='⛌ Отменить ввод')
        )
        return
    elif is_used:
        text = '💢 <b>Вы уже использовали данный промокод ранее, попробуйте другой!</b>'
        reply_markup = kb.back_to_product(product_id)
    elif promocode.type.value not in ['discount_percent', 'discount_fix']:
        await message.answer('❌')
        text = """⚠️ <b>Введённый промокод не подходит для покупки!</b>

▼ Для активации промокода введите его в профиле"""
        reply_markup = kb.back_to_profile(product_id)
    else:
        discount, discount_type = promocode.content, promocode.type.value
        if discount_type == 'discount_fix':
            new_product_price = product_price - discount
        else:
            new_product_price = round(product_price * ((100 - discount) / 100), 1)
        text = texts['ru']['catalog']['success_promo'](product_price, new_product_price, product.name)
        reply_markup = kb.build_buy_product_with_promocode(product_id, promocode.name)
        await state.clear()
    await message.answer(text=text, reply_markup=reply_markup)


# ======== BUY HANDLER ========
@router.callback_query(BuyProductCallback.filter(), StateFilter(default_state))
async def buy_product_cmd(call: CallbackQuery, callback_data: BuyProductCallback, bot: Bot):
    product_id = callback_data.id
    promocode = callback_data.promocode

    async with async_session() as session:
        promocode = await PromocodeRepo(session).get_promocode_by_name(promocode)
        if promocode:
            is_used = await UserPromocodeRepo(session).check_promo(call.from_user.id, promocode.name)
        product = await ProductRepo(session).get_product(product_id)
        product_price = product.price
        user = await UserRepo(session).get_user(call.from_user.id)
        balance = user.balance
    # ==== CALCULATE NEW PRICE & VALIDATE PROMO ==== #
    if promocode is not None:
        if promocode.type.value == 'balance':
            await call.answer('Неверный промокод ❌')
            return
        elif is_used:
            await call.answer('Вы уже использовали данный промокод ранее')
            return
        elif promocode.type.value == 'discount_fix':
            product_price = max(0, product_price - promocode.content)
        elif promocode.type.value == 'discount_percent':
            product_price = round(product_price * (100 - promocode.content) / 100, 3)
    # ==== CHECK CONTENT AVAILABLE ==== #
    if len(product.content) == 0:
        await call.answer('Нет в наличии ❌')
        return
    # ==== CHECK BALANCE AVAILABLE ==== #
    if balance < product_price:
        await call.answer(
            text=texts['ru']['catalog']['low_balance'](round(product_price - balance, 0)),
            show_alert=True
        )
        return

    async with async_session() as session:
        content = await ProductRepo(session).get_product_content(product_id)
        if content:
            purchase_id = await UserPurchasesRepo(session).add_purchase(
                tg_id=call.from_user.id,
                amount=product_price,
                name=product.name,
                content=content
            )
            await UserRepo(session).update_balance(call.from_user.id, -product_price)
            channels = await NotifyChannelRepo(session).get_channels()
            if promocode:
                await UserPromocodeRepo(session).add_promo(call.from_user.id, promocode.name)
                await PromocodeRepo(session).post_activation(promocode.name)

    if not content:
        await call.answer(texts['ru']['catalog']['content_not_available'])
        return
    await TgAdminLogService(bot, call.from_user.id, call.from_user.username, channels).send_purchase(
        amount=product_price,
        product_name=product.name)
    if promocode:
        await TgAdminLogService(bot, call.from_user.id, call.from_user.username, channels).send_promocode(
            promocode=promocode.name,
            promocode_type=promocode.type)
    await call.message.delete()
    await call.message.answer_document(
        document=BufferedInputFile(
            BytesIO(content.encode("utf-8")).read(),
            filename=f"{product.name}.txt"
        ),
        caption=texts['ru']['catalog']['success_purchase'](purchase_id), reply_markup=kb.success_buy
    )
    logger.info(f'New success product buy from user={call.from_user.id}')
