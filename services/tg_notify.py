import asyncio
from aiogram import Bot


class NotifyService:
    tasks = {}

    async def add_task(self, tg_id: int, text: str, bot: Bot, delay: int) -> int:
        task_id = len(self.tasks) - 1 + 1
        task = asyncio.create_task(
            self.__send_sms(
                bot=bot,
                tg_id=tg_id,
                text=text,
                delay=delay,
                task_id=task_id
            )
        )
        self.tasks.setdefault(tg_id, []).append(task)
        return task_id

    async def del_task(self, tg_id: int, task_id: int):
        try:
            del self.tasks[tg_id][task_id]
        except IndexError:
            ...

    async def __send_sms(self, bot: Bot, tg_id: int, text: str, delay: int, task_id: int):
        await asyncio.sleep(delay)
        await bot.send_message(
            chat_id=tg_id,
            text=text,
            disable_web_page_preview=True
        )
        del self.tasks[tg_id][task_id]
        if not self.tasks[tg_id]:
            del self.tasks[tg_id]


notify_service = NotifyService()
