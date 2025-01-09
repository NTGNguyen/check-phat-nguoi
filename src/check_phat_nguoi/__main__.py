import asyncio
from logging import getLogger

from truststore import inject_into_ssl

from check_phat_nguoi import GetData, SendNotifications
from check_phat_nguoi.config.config_reader import config

from .utils.setup_logger import setup_logger

logger = getLogger(__name__)


async def async_main() -> None:
    inject_into_ssl()
    setup_logger()
    logger.debug(f"Config read: {config}")
    await GetData().get_data()
    await SendNotifications().send()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
