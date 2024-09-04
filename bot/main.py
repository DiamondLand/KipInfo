import configparser
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from tortoise import Tortoise, run_async
from loguru import logger

from events import error_handler
from handlers import commands_handler, different_types, mailing


config = configparser.ConfigParser()
config.read("config.ini")

bot = Bot(config["SETTINGS"]["testing_token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.config = config
bot.ADMINS_IDS = [872278858, 767922691]

dp = Dispatcher()


# --- Подгрузка модулей --- #
async def main():
    # Настройка конфигурации логгера
    logging.basicConfig(
        filename='logs/autoBot.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logger.info("Loading modules...")
    dp.include_routers(
        error_handler.router,
        commands_handler.router,
        mailing.router,
        different_types.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logger.success("Successfully launched")
    await dp.start_polling(bot)


async def init_db():
    await Tortoise.init(
        db_url='sqlite://assets/db/database.db',
        modules={'models': ['database.models']}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init_db())
    asyncio.run(main())
