from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters.state import StateFilter

from tg_bot.infra.database import async_session

from tg_bot.adminka.keyboards import promocodes as kb
from tg_bot.adminka.states.promocodes import *
from tg_bot.adminka.callbacks.promocodes import *
from tg_bot.adminka.repositories.promocodes import PromocodeRepo

from tg_bot.adminka.callbacks.main import PromocodeCallback
from tg_bot.adminka.keyboards.main import back_to_admin_kb

router = Router()

promocodes_types = {
    'balance': 'Баланс',
    'discount_fix': 'Фиксированная скидка на покупку',
    'discount_percent': 'Процентная скидка на покупку'
}

promocodes_types_content = {
    'balance': '₽',
    'discount_fix': '₽',
    'discount_percent': '%'
}


@router.callback_query(
    PromocodeCallback.filter(),
    StateFilter(
        default_state,
        PromocodeStates.new_name,
        PromocodeStates.new_type,
        PromocodeStates.new_quantity
    )
)
async def promocode_panel_cmd(call: CallbackQuery, state: FSMContext):
    await state.clear()
    async with async_session() as session:
        promocodes = await PromocodeRepo(session).get_promocodes()
    await call.message.edit_text(
        'Выберите действие',
        reply_markup=kb.build_promocode_panel(promocodes)
    )


@router.callback_query(NewPromocodeCallback.filter(), StateFilter(default_state))
async def new_promocode_cmd(call: CallbackQuery, state: FSMContext):
    await state.set_state(PromocodeStates.new_name)
    await call.message.edit_text(
        'Введите название для нового промокода',
        reply_markup=kb.back_to_promo_panel
    )


@router.message(StateFilter(PromocodeStates.new_name))
async def new_promocode_name_cmd(message: Message, state: FSMContext):
    promocode = message.text
    async with async_session() as session:
        is_exists = await PromocodeRepo(session).get_promocode_by_name(promocode)
    if is_exists:
        await message.answer('Промокод с таким названием существует, попробуйте новый',
                             reply_markup=kb.back_to_promo_panel)
        return
    await state.update_data({'name': message.text})
    await state.set_state(PromocodeStates.new_type)
    await message.answer(
        'Выберите тип промокода',
        reply_markup=kb.promocode_type_select
    )


@router.callback_query(PromocodeTypeCallback.filter(), StateFilter(PromocodeStates.new_type))
async def new_promocode_type_cmd(call: CallbackQuery, callback_data: PromocodeTypeCallback, state: FSMContext):
    type = callback_data.type
    await state.update_data({
        'type': type
    })
    await state.set_state(PromocodeStates.new_content)
    await call.message.edit_text(
        'Отлично! А теперь пришлите размер скидки для указанного типа',
        reply_markup=kb.back_to_promo_panel
    )


@router.message(StateFilter(PromocodeStates.new_content))
async def new_promocode_content(message: Message, state: FSMContext):
    type = await state.get_value('type')
    try:
        content = float(message.text)
        if type == 'discount_percent' and content >= 100:
            await message.answer(
                f'Вы указали процентную скидку: {content}\n'
                f'Она не может быть больше 100, попробуйте снова',
                reply_markup=kb.back_to_promo_panel
            )
            return
    except ValueError:
        await message.answer(
            'Скидка должна быть числом! Попробуйте снова',
            reply_markup=kb.back_to_promo_panel
        )
        return
    await state.update_data({'content': content})
    await message.answer(
        f'Тип промокода: {promocodes_types[type]}\n'
        f'Скидка: <code>{content}{promocodes_types_content[type]}</code>'
    )
    await state.set_state(PromocodeStates.new_quantity)
    await message.answer(
        'Отлично! А теперь пришлите кол-во промокодов которое будет создано',
        reply_markup=kb.back_to_promo_panel
    )


@router.message(StateFilter(PromocodeStates.new_quantity))
async def new_promocode_quantity(message: Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer(
            'Кол-во промокодов должно быть целым числом! Попробуйте снова',
            reply_markup=kb.back_to_promo_panel
        )
        return
    data = await state.get_data()
    async with async_session() as session:
        await PromocodeRepo(session).add_promocode(
            name=data['name'],
            quantity=quantity,
            type=data['type'],
            content=data['content']
        )
    await state.clear()
    await message.answer(
        'Промокод был успешно добавлен!',
        reply_markup=kb.back_to_promo_panel
    )


@router.callback_query(PromocodeItemCallback.filter(), StateFilter(default_state))
async def promocode_item_panel(call: CallbackQuery, callback_data: PromocodeItemCallback):
    promocode = callback_data.name
    async with async_session() as session:
        promocode = await PromocodeRepo(session).get_promocode_by_name(promocode)
    await call.message.edit_text(
        f'Промокод: <b><i>{promocode.name}</i></b>\n'
        f'\n'
        f'Тип промокода: {promocodes_types[promocode.type.value]}\n'
        f'Скидка: <code>{promocode.content}{promocodes_types_content[promocode.type.value]}</code>\n'
        f'Оставшиеся кол-во активаций: <code>{promocode.activations}</code>',
        reply_markup=kb.build_promocode_item_panel(promocode.name)
    )


@router.callback_query(DelPromocodeCallback.filter(), StateFilter(default_state))
async def del_promocode_item(call: CallbackQuery, callback_data: DelPromocodeCallback):
    name = callback_data.name
    await call.message.edit_text(
        'Вы уверены что хотите удалить  промокод? Его нельзя будет активировать',
        reply_markup=kb.build_confirm_del_promocode(name)
    )


@router.callback_query(ConfirmDelPromocode.filter(), StateFilter(default_state))
async def confirm_del_promocode(call: CallbackQuery, callback_data: ConfirmDelPromocode):
    action, name = callback_data.action, callback_data.name
    if not action:
        await call.message.edit_text(
            'Отменено',
            reply_markup=kb.back_to_promo_item_panel(name)
        )
    else:
        async with async_session() as session:
            await PromocodeRepo(session).del_promocode(name)
        await call.message.edit_text(
            'Удалено',
            reply_markup=kb.back_to_promo_panel
        )
