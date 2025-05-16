from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from asyncio import run

from tg_bot.config import bot_settings, is_reset_database
from tg_bot.infra.log import logger
from tg_bot.infra.database import reset_database

from tg_bot.handlers import router

from tg_bot.middleware.is_blocked import IsUserBlockedMiddleware
from tg_bot.middleware.rps_middleware import RpsMiddleware
from tg_bot.middleware.is_subscribed import IsSubscribedMiddleware


async def main():
    print("""
  ______          __        ____           ______                         
  / ____/___  ____/ /__     / __ )__  __   / ____/__  ____  _________ ____ 
 / /   / __ \/ __  / _ \   / __  / / / /  / / __/ _ \/ __ \/ ___/ __ `/ _ \\
/ /___/ /_/ / /_/ /  __/  / /_/ / /_/ /  / /_/ /  __/ /_/ / /  / /_/ /  __/
\____/\____/\__,_/\___/  /_____/\__, /   \____/\___/\____/_/   \__, /\___/ 
                               /____/                         /____/
    """)

    logger.info("Starting setup bot...")

    if is_reset_database:
        logger.info('Database on_startup loading...')
        await reset_database()

    dp = Dispatcher()
    bot = Bot(
        token=bot_settings.BOT_API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.delete_webhook()
    await bot.set_my_commands(commands=[
        BotCommand(command="/start", description="Перезапустить бота"),
    ])

    dp.include_router(router)
    dp.update.middleware(IsUserBlockedMiddleware())
    dp.update.middleware(IsSubscribedMiddleware(bot))
    dp.update.middleware(RpsMiddleware())

    logger.info("Bot started!")
    await bot.send_message(
        chat_id=1190261959,
        text='George, я запустился🐠' if is_reset_database is False else 'George, я запустился c ресетом дб🐠'
    )
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        logger.info('Bot finished')
