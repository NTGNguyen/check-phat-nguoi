import asyncio

from check_phat_nguoi.get_data import GetData
from check_phat_nguoi.notify import SendNotifications

from .utils.setup_logger import setup_logger


async def async_main() -> None:
    setup_logger()
    await GetData().get_data()
    await SendNotifications().send()


def main() -> None:
    asyncio.run(async_main())


__all__ = ["main"]
