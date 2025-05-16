from aiogram import Bot
from tg_bot.infra.database.models import NotifyChannel, Promocode
from tg_bot.infra.log import logger

from datetime import datetime


class TgAdminLogService:

    def __init__(self, bot: Bot, user_tg_id: int, username: str, channels: NotifyChannel):
        self.bot = bot
        self.channels = channels
        self.user_tg_id = user_tg_id
        self.username = '@' + username if username else 'отсутствует'

    async def __send(self, text, channel_id):
        if channel_id:
            try:
                await self.bot.send_message(
                    chat_id=channel_id,
                    text=text,
                )
            except Exception as e:
                logger.warn(f'ERROR DURING SENDING LOG e=[{e}]')

    async def send_purchase(self, amount, product_name):
        text = f"""🛍 <b><i>НОВАЯ ПОКУПКА</i></b>
        
💸 Сумма: <code>{amount}</code>
🏛 Товар: <b>{product_name}</b>

🔎 Юзер id: <code>{self.user_tg_id}</code>
🦣 Юзернейм: {self.username}"""
        await self.__send(text=text, channel_id=self.channels.payment)

    async def send_promocode(self, promocode: Promocode, promocode_type):
        text = f"""🎟 <b><i>НОВАЯ АКТИВАЦИЯ</i></b>
        
🎫 Промокод: {promocode}
🧩 Тип: {promocode_type.value}

🔎 Юзер id: <code>{self.user_tg_id}</code>
🦣 Юзернейм: {self.username}"""
        await self.__send(text=text, channel_id=self.channels.payment)

    async def send_payment(self, amount, system, status):
        text = f"""🔐 <b><i>НОВАЯ ТРАНЗАКЦИЯ</i></b>
        
💸Сумма: <code>{amount}</code>
🏛 Платежная система: <b>{system}</b>
✏️ Статус: {status}

🔎 Юзер id: <code>{self.user_tg_id}</code>
🦣 Юзернейм: {self.username}
"""
        await self.__send(text=text, channel_id=self.channels.payment)

    async def send_new_user(self, ref_link: str):
        text = f"""👤 <b><i>НОВЫЙ ЮЗЕР</i></b>
        
📅Дата регистрации: {datetime.now().strftime("%d.%m.%Y")}
🧷Реферальная ссылка: {ref_link}

🔎Юзер id: <code>{self.user_tg_id}</code>
🦣 Юзернейм: {self.username}"""
        await self.__send(text=text, channel_id=self.channels.new_user)
