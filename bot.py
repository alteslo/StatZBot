import asyncio
import logging

import gspread_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.common import register_common
from tgbot.handlers.stat_data_proc import register_analysis
from tgbot.handlers.litrev import register_lit_rev
from tgbot.handlers.return_back import register_return
from tgbot.handlers.presentation import register_presentation
from tgbot.middlewares.db import DbMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_common(dp)
    register_analysis(dp)
    register_lit_rev(dp)
    register_presentation(dp)
    register_return(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2(config.redis.host) if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    google_client_manager = gspread_asyncio.AsyncioGspreadClientManager(
        config.misc.scoped_credentials
    )
    gsheet_key = config.misc.gsheet_key
    bot['config'] = config
    bot['google_client_manager'] = google_client_manager
    bot['gsheet_key'] = gsheet_key

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
