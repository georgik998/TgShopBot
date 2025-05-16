from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import default_state

from json import dumps

from tg_bot.keyboards import payment as kb
from tg_bot.callbacks.main import PaymentCallback
from tg_bot.callbacks.payment import PaymentSystemCallback, PaymentAmountCallback

from tg_bot.repositories.content import TextRepo, BannerRepo, NotifyChannelRepo, ContactsRepo
from tg_bot.services.tg_admin_log import TgAdminLogService
from tg_bot.services.tg_notify import notify_service

from tg_bot.infra.database import async_session
from tg_bot.states.payment import PaymentStates

from tg_bot.infra.log import logger

from tg_bot.repositories.payment import PaymentRepo

from tg_bot.services.payment import cryptobot_api

router = Router()


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
        reply_markup=kb.payment_amounts
    )


@router.callback_query(F.data == 'payment_another', StateFilter(PaymentStates.amount))
async def payment_another(call: CallbackQuery):
    await call.answer('⚡️ Теперь укажите в сообщении сумму, на которую хотите пополнить баланс и отправьте боту',
                      show_alert=True)


@router.callback_query(PaymentCallback.filter(), StateFilter(default_state, PaymentStates.amount))
async def payment_callback_cmd(call: CallbackQuery, state: FSMContext, bot: Bot):
    async with async_session() as session:
        payment_text = await TextRepo(session).get_text('payment')
        payment_banner = await BannerRepo(session).get('payment')
    await state.set_state(PaymentStates.amount)
    if call.message.photo:
        message = await call.message.edit_caption(
            caption=payment_text,
            reply_markup=kb.payment_amounts
        )
    else:
        message = await call.message.edit_media(
            media=InputMediaPhoto(
                caption=payment_text,
                media=payment_banner
            ),
            reply_markup=kb.payment_amounts
        )



@router.message(StateFilter(PaymentStates.amount))
async def payment_custom_amount_cmd(message: Message, state: FSMContext):
    amount = message.text
    try:
        amount = float(amount)
    except ValueError:
        await message.answer(
            'Сумма должна быть целым числом!',
            reply_markup=kb.back_to_payment
        )
        return
    if amount < 50:
        await message.answer('❌')
        await message.answer(
            text="""💢 <i>Минимальная сумма пополнения 50₽</i>

▼ Отмените ввод / Введите новую сумму пополнения:""",
            reply_markup=kb.build_back_to_payment(style='⛌ Отменить ввод')
        )
        return
    async with async_session() as session:
        payment_banner = await BannerRepo(session).get('payment')
    await state.clear()
    await message.answer_photo(
        photo=payment_banner,
        caption=f"""💳 Пополнение баланса

Сумма к оплате: {amount}₽
Выберите платежный метод""",
        reply_markup=kb.build_payment_system(amount=amount)
    )


@router.callback_query(PaymentAmountCallback.filter(), StateFilter(PaymentStates.amount))
async def payment_fix_amount_cmd(call: CallbackQuery, callback_data: PaymentAmountCallback, state: FSMContext):
    amount = callback_data.amount
    await state.clear()
    await call.message.edit_caption(
        caption=f"""💳 Пополнение баланса
Сумма к оплате: {amount}₽
Выберите платежный метод""",
        reply_markup=kb.build_payment_system(amount=amount)
    )


@router.callback_query(PaymentSystemCallback.filter(), StateFilter(default_state))
async def payment_system_cmd(call: CallbackQuery, callback_data: PaymentSystemCallback, bot: Bot):
    if callback_data.amount < 1000 and callback_data.system == 'nicepay':
        await call.answer(
            '💢 Сумма должна быть более 1000 RUB, выберите другой метод пополнения', show_alert=True
        )
        return
    await call.answer(
        'Здесь будет форма оплаты когда одобрят апи', show_alert=True
    )
    return
    from pydantic import BaseModel
    class Invoice(BaseModel):
        invoice_id: int
        bot_invoice_url: str

    amount = callback_data.amount
    system = callback_data.system

    # payment_info = await cryptobot_api.create_invoice(
    #     amount=amount,
    #     fiat='RUB',
    #     currency_type='fiat',
    #     description='Описание',
    #     payload=dumps({
    #         'tg_id': call.from_user.id,
    #         'tg_username': call.from_user.username if call.from_user.username else None,
    #     }),
    #     allow_anonymous=True,
    #     expires_in=10 * 60
    # )
    payment_info = Invoice(
        invoice_id=777,
        bot_invoice_url='https://t.me/Gyukkvf_bot'
    )
    logger.info(f'Transaction: status=created amount={amount} system={system}')

    async with async_session() as session:
        contacts = await ContactsRepo(session).get_contacts()
        channels = await NotifyChannelRepo(session).get_channels()
        await PaymentRepo(session).post(
            tg_id=call.from_user.id,
            system=system,
            system_id=str(payment_info.invoice_id),
            amount=amount
        )
    await TgAdminLogService(
        bot=bot,
        user_tg_id=call.from_user.id,
        username=call.from_user.username,
        channels=channels
    ).send_payment(amount=amount, system=system.upper(), status='created')

    notify_task_id = await notify_service.add_task(
        tg_id=call.from_user.id,
        bot=bot,
        delay=10,
        text=f"""⚠️ У заказа <code>{payment_info.invoice_id}</code> истек срок оплаты

Если у вас возникла одна из проблем:
🔹 Не зачислилась оплата
🔹 Не выдались реквизиты
🔹 Не вышло сделать перевод

<b>Обратитесь к поддержке платежной системы</b>
{contacts.support.replace('https://t.me/', '@')}


❤️ Приносим свои извинения, если вы столкнулись с проблемами при оплате. 
С радостью поможем решить их вам!"""
    )
    await call.message.edit_caption(
        caption='Счет создан, у вас есть 5 минут чтобы оплатить',
        reply_markup=kb.payment(payment_info.bot_invoice_url, contacts.support)
    )
    # async with async_session() as session:
    #     channels = await NotifyChannelRepo(session).get_channels()
    #     await UserRepo(session).update_balance(call.from_user.id, amount)
    #     user = await UserRepo(session).get_user(call.from_user.id)
    #     if user.father_id:
    #         await UserRepo(session).update_balance(user.father_id, float(round(amount * 0.05, 3)))
    # await NotifyService(
    #     bot=bot,
    #     user_tg_id=call.from_user.id,
    #     username=call.from_user.username,
    #     channels=channels
    # ).send_payment(amount=amount, system=system.upper(), status='success')
    # logger.info(f'Transaction: status=success amount={amount} system={system}')
    # await call.message.delete()
    # await call.message.answer('🎉')
    # await call.message.answer(
    #     text=f'💸Ваш баланс пополнен на <code>{amount}₽</code> !',
    #     reply_markup=kb.success_payment
    # )
