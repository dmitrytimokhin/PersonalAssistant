import os
from pathlib import Path
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import asyncio
import contextlib
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from redis.asyncio.client import Redis
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers import base_router, user_router
from aioutils import set_commands

load_dotenv()
MAIN_ADMIN = int(os.getenv("MAIN_ADMIN_ID"))

Path('LOGS/').mkdir(parents=True, exist_ok=True)
logging.basicConfig(format="%(asctime)s - [%(levelname)s] -  %(funcName)s - %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S",
                    level=logging.DEBUG)
logger = logging.getLogger('MAIN')

file_formater = Formatter(fmt="%(asctime)s - [%(levelname)s] -  %(name)s - "
                              "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
                          datefmt="%d/%m/%Y %H:%M:%S")
file_handler = RotatingFileHandler(filename='./LOGS/MAIN.log',
                                   maxBytes=500000,
                                   backupCount=3,
                                   encoding='utf-8')
# Уровень логирования в LOGS
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


async def start_bot(bot: Bot):
    await set_commands(bot)
    try:
        await bot.send_message(chat_id=MAIN_ADMIN, text='The Bot is running!')
        logger.debug(msg='The Bot is running!')
    except Exception as ex:
        logger.error(f'[Exception] - {ex}', exc_info=True)


async def stop_bot(bot: Bot):
    try:
        await bot.send_message(chat_id=MAIN_ADMIN, text='The Bot is stopped!')
        logger.debug(msg='The Bot is stopped!')
    except Exception as ex:
        logger.error(msg=f'[Exception] - {ex}', exc_info=True)


async def main(clear: bool = False):
    Path('data/').mkdir(parents=True, exist_ok=True)
    logger.info("Started!")

    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook()
    dp_storage = MemoryStorage()
#    storage = RedisStorage(redis=Redis, state_ttl=3600, data_ttl=3600)
#    dp_storage = storage.from_url('redis://localhost:6379/1')
    dp = Dispatcher(storage=dp_storage)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.include_routers(user_router, base_router)
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(msg=f'[Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()
        await dp.storage.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
