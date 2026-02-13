import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()


async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.delete_webhook(drop_pending_updates=True)


    # dp.update.middleware(DataBaseSession(session_pool=session_maker)) слой для сессии

    logging.basicConfig(level=logging.INFO)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Выход')

