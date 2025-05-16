from aiogram import Bot

from tg_bot.config import bot_settings
from typing import Tuple, Union

from typing import Sequence

from tg_bot.infra.database.models import SubscribeChannel


async def check_subscribe(channels: Sequence[SubscribeChannel], user_id: int, bot: Bot):
    no_subscribe_channels_urls = []
    for channel in channels:
        chat_member = await bot.get_chat_member(channel.channel_id, user_id)
        if chat_member.status not in ["member", "administrator", "creator"]:
            no_subscribe_channels_urls.append(channel.channel_url)
    return no_subscribe_channels_urls


SPLIT_SYMBOL = '_'


def create_product_link(product_id, father_id):
    return f'{bot_settings.BOT_URL}?start={father_id}{SPLIT_SYMBOL}{product_id}'


def parse_link(args) -> Union[Tuple[int, int], Tuple[None, None]]:
    try:
        father_id, product_id = map(int, args.split(SPLIT_SYMBOL))
        return father_id, product_id
    except Exception:
        return None, None


def round_number(num):
    num = float(num)
    num = round(num, 1)
    return int(num) if num.is_integer() else num
