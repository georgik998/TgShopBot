from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from html import escape

from tg_bot.adminka.callbacks.main import RefLinksCallback
from tg_bot.adminka.callbacks.ref_link import *
from tg_bot.adminka.keyboards import ref_links as kb

from tg_bot.infra.database import async_session
from tg_bot.adminka.repositories.ref_links import RefLinkRepo
from tg_bot.adminka.states.ref_link import EditRefLink

from tg_bot.config import bot_settings

router = Router()


@router.callback_query(RefLinksCallback.filter(), StateFilter(default_state))
async def ref_links_panel_cmd(call: CallbackQuery):
    async with async_session() as session:
        links = await RefLinkRepo(session).get_all()
    await call.message.edit_text(
        '💈 Панель управления рекламными ссылками\n'
        '\n'
        '✍️ Кликнете на <b>любой параметр</b> ссылки чтобы открыть полную панель управления',
        reply_markup=kb.ref_links_manage_panel(links)
    )


@router.callback_query(NewRefLinkCallback.filter(), StateFilter(default_state))
async def new_ref_link_cmd(call: CallbackQuery):
    async with async_session() as session:
        link_id = await RefLinkRepo(session).post()
        links = await RefLinkRepo(session).get_all()
    await call.message.answer(
        f'✅ Новая ссылка:\n'
        f'{bot_settings.BOT_URL}?start=ref{link_id}'
    )
    await call.message.edit_text(
        '💈 Панель управления рекламными ссылками\n'
        '\n'
        '✍️ Кликнете на <b>любой параметр</b> ссылки чтобы открыть полную панель управления',
        reply_markup=kb.ref_links_manage_panel(links)
    )


@router.callback_query(EditRefLinkCallback.filter(), StateFilter(default_state, EditRefLink.label))
async def edit_ref_link_panel_cmd(call: CallbackQuery, callback_data: EditRefLinkCallback, state: FSMContext):
    id = callback_data.id
    async with async_session() as session:
        ref_link = await RefLinkRepo(session).get_by_id(id)
    await state.clear()
    await call.message.edit_text(
        text=f"""💠Рекламная ссылка:
{bot_settings.BOT_URL}?start=ref{ref_link.id}
📍Метка:
<blockquote>{escape(ref_link.label)}</blockquote>

👤Пришло юзеров по ссылке: <b><i>{ref_link.invited} человек</i></b>
💸Пополнена баланса на: <code>{ref_link.income}₽</code>
""",
        reply_markup=kb.edit_ref_link(ref_link)
    )


# ======== Edit label ======= #
@router.callback_query(EditLabelRefLinKCallback.filter(), StateFilter(default_state))
async def edit_label_ref_link_cmd(call: CallbackQuery, callback_data: EditRefLinkCallback, state: FSMContext):
    id = callback_data.id
    await state.update_data({'id': id})
    await state.set_state(EditRefLink.label)
    await call.message.edit_text(
        'Пришлите новую метку для ссылки',
        reply_markup=kb.back_to_edit_ref_link_button(id)
    )


@router.message(EditRefLink.label)
async def update_label_ref_link_cmd(message: Message, state: FSMContext):
    label = message.text
    id = await state.get_value('id')
    if not label or len(label) > 512:
        await message.answer(
            'Максимальная длина метки 512 символа, попробуй снова',
            reply_markup=kb.back_to_edit_ref_link_button(id)
        )
        return
    async with async_session() as session:
        await RefLinkRepo(session).patch_label(id=id, label=label)
        ref_link = await RefLinkRepo(session).get_by_id(id)
    await state.clear()
    await message.answer(
        text=f"""💠Рекламная ссылка:
{bot_settings.BOT_URL}?start=ref{ref_link.id}
📍Метка:
<blockquote>{escape(ref_link.label)}</blockquote>

👤Пришло юзеров по ссылке: <b><i>{ref_link.invited}</i></b>
💸Пополнена баланса на: <code>{ref_link.income}₽</code>
    """,
        reply_markup=kb.edit_ref_link(ref_link)
    )


# ======== Reset statistic======= #
@router.callback_query(ResetRefLinkCallback.filter(), StateFilter(default_state))
async def reset_ref_link_cmd(call: CallbackQuery, callback_data: ResetRefLinkCallback):
    id = callback_data.id
    await call.message.edit_text(
        'Вы уверены что хотите сбросить статистику по ссылке?',
        reply_markup=kb.reset_ref_link_cmd(id)
    )


@router.callback_query(ConfirmResetRefLinkCallback.filter(), StateFilter(default_state))
async def cofirm_reset_ref_link(call: CallbackQuery, callback_data: ConfirmResetRefLinkCallback):
    id, action = callback_data.id, callback_data.action
    if action:
        await call.answer('✅ Статистика сброшена')
        async with async_session() as session:
            await RefLinkRepo(session).delete_statistic_by_id(id)
            ref_link = await RefLinkRepo(session).get_by_id(id)
    else:
        await call.answer('❌ Отменено')
        async with async_session() as session:
            ref_link = await RefLinkRepo(session).get_by_id(id)
    await call.message.edit_text(
        text=f"""💠Рекламная ссылка:
{bot_settings.BOT_URL}?start=ref{ref_link.id}
📍Метка:
<blockquote>{escape(ref_link.label)}</blockquote>

👤Пришло юзеров по ссылке: <b><i>{ref_link.invited} человек</i></b>
💸Пополнена баланса на: <code>{ref_link.income}₽</code>""",
        reply_markup=kb.edit_ref_link(ref_link)
    )


# ======== Delete ======= #
@router.callback_query(DelRefLinkCallback.filter(), StateFilter(default_state))
async def del_ref_link_cmd(call: CallbackQuery, callback_data: DelRefLinkCallback):
    id = callback_data.id
    await call.message.edit_text(
        'Вы уверены что хотите удалить ссылку?',
        reply_markup=kb.del_ref_link_cmd(id)
    )


@router.callback_query(ConfirmDelRefLinkCallback.filter(), StateFilter(default_state))
async def confirm_del_ref_link_cmd(call: CallbackQuery, callback_data: ConfirmDelRefLinkCallback):
    action, id = callback_data.action, callback_data.id
    if action:
        async with async_session() as session:
            await RefLinkRepo(session).delete_by_id(id)
        await call.message.edit_text(
            '🗑 Удалено',
            reply_markup=kb.bact_to_ref_link
        )
    else:
        async with async_session() as session:
            ref_link = await RefLinkRepo(session).get_by_id(id)
        await call.answer('❌ Отменено')
        await call.message.edit_text(
            text=f"""💠Рекламная ссылка:
{bot_settings.BOT_URL}?start=ref{ref_link.id}
📍Метка:
<blockquote>{escape(ref_link.label)}</blockquote>

👤Пришло юзеров по ссылке: <b><i>{ref_link.invited}</i></b>
💸Пополнена баланса на: <code>{ref_link.income}₽</code>""",
            reply_markup=kb.edit_ref_link(ref_link)
        )
