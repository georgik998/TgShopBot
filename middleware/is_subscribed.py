from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest

from typing import Any

from tg_bot.infra.database import async_session
from tg_bot.repositories.content import SubscribeChannelRepo
from tg_bot.keyboards.main import channel_to_subscribe

from tg_bot.utils import *
from tg_bot.config import bot_settings

from tg_bot.services.tg_admin_log import TgAdminLogService
from tg_bot.repositories.content import NotifyChannelRepo
from tg_bot.repositories.user import UserRepo
from tg_bot.repositories.ref_links import RefLinkRepo


async def new_user(tg_id, tg_username, bot, ref_link):
    father_id = None
    ref_link_id = None
    try:
        # ref_link: '/start 1190261959_11' or '/start'
        # / start ref1190261959
        # / start ref = 1190261959
        # /start refDSJO0lTH
        father_id = int(ref_link.split(' ')[1].split('_')[0])
    except IndexError:
        pass
    except ValueError:
        pass
    if not father_id:
        try:
            ref_link_id = ref_link.split(' ')[1].replace('ref', '')
        except IndexError:
            pass
        except ValueError:
            pass

    async with async_session() as session:
        if ref_link_id:
            is_ref_link_exist = await RefLinkRepo(session).is_exist(ref_link_id)
            if not is_ref_link_exist:
                ref_link_id = None
        new_user = await UserRepo(session).post_user(tg_id=tg_id, father_id=father_id, ref_link_id=ref_link_id)
        if new_user:
            notify_channels = await NotifyChannelRepo(session).get_channels()
            if ref_link_id:
                await RefLinkRepo(session).add_activation(ref_link_id)
    if new_user:
        if father_id:
            ref_link = bot_settings.BOT_URL + f'?start={father_id}'
        elif ref_link_id:
            ref_link = f'{bot_settings.BOT_URL}?start=ref{ref_link_id}'
        else:
            ref_link = 'отсутствует'
        await TgAdminLogService(
            bot=bot,
            user_tg_id=tg_id,
            username=tg_username,
            channels=notify_channels
        ).send_new_user(ref_link=ref_link)


class IsSubscribedMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(
            self,
            handler,
            event,
            data
    ) -> Any:
        # Если команда страт
        if event.message and event.message.text and event.message.text.startswith('/start'):
            await new_user(
                tg_id=data['event_from_user'].id,
                tg_username=data['event_from_user'].username,
                bot=self.bot,
                ref_link=event.message.text
            )
        user_id = data['event_from_user'].id
        async with async_session() as session:
            channels = await SubscribeChannelRepo(session).get_channels()
        no_subscribe_channels_urls = await check_subscribe(channels=channels, user_id=user_id, bot=self.bot)
        if no_subscribe_channels_urls:
            if event.message:
                await event.message.answer(
                    text='Вы не дописаны на нужные каналы, чтобы пользоваться ботом, подпишитесь на них',
                    reply_markup=channel_to_subscribe(no_subscribe_channels_urls)
                )
                return
            else:
                if event.callback_query.message.photo:
                    await event.callback_query.message.delete()
                    await event.callback_query.message.answer(
                        text='Вы не дописаны на нужные каналы, чтобы пользоваться ботом, подпишитесь на них',
                        reply_markup=channel_to_subscribe(no_subscribe_channels_urls)
                    )
                else:
                    try:
                        await event.callback_query.message.edit_text(
                            text='Вы не дописаны на нужные каналы, чтобы пользоваться ботом, подпишитесь на них',
                            reply_markup=channel_to_subscribe(no_subscribe_channels_urls)
                        )
                    except TelegramBadRequest:
                        await event.callback_query.answer('❌Вы не подписаны на каналы')
                        return
                    return
        return await handler(event, data)
