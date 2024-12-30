import asyncio
from logging import Logger, getLogger

from check_phat_nguoi.config import config
from check_phat_nguoi.config.config_reader import _config_reader
from check_phat_nguoi.get_data.check_phat_nguoi import GetDataCheckPhatNguoi

from .utils.setup_logger import setup_logger

logger: Logger = getLogger(__name__)


async def _main():
    setup_logger()
    logger.debug(config)
    get_data_object = GetDataCheckPhatNguoi(_config_reader().data)
    data = await get_data_object.get_data()


def main():
    asyncio.run(_main())


__all__ = ["main"]
