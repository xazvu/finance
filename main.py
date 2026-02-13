import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from bot.db.engine import create_db, drop_db
from bot.user import router as user_router
from bot.middlewere import DataBaseSession
from bot.db.engine import session_maker

load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()
dp.include_router(user_router)

async def on_startup(bot):

    # await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.delete_webhook(drop_pending_updates=True)


    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    logging.basicConfig(level=logging.INFO)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Выход')

