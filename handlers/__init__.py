from aiogram import Router

from tg_bot.handlers.user import router as user_router
from tg_bot.adminka import router as adminka_router

router = Router()

router.include_routers(
    user_router,
    adminka_router

)

# from aiogram.types import Message
#
#
# @router.message()
# async def message(sms: Message):
#     await sms.answer(
#         sms.photo[-1].file_id
#     )
