import asyncio
from logging import getLogger

from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.get_data import GetData
from check_phat_nguoi.notify import SendNotifications

from .utils.setup_logger import setup_logger

logger = getLogger(__name__)


async def async_main() -> None:
    setup_logger()
    logger.debug(f"Config read: {config}")
    await GetData().get_data()
    await SendNotifications().send()


def main() -> None:
    asyncio.run(async_main())


__all__ = ["main"]
