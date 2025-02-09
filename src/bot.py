import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import index
from config import BOT_TOKEN

import logging
logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dispatch = Dispatcher(storage=storage)
    dispatch.include_router(index.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatch.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
