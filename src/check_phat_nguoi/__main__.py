import asyncio
from logging import getLogger

from check_phat_nguoi.config_reader import config
from check_phat_nguoi.context import plates_context
from check_phat_nguoi.get_data import GetData
from check_phat_nguoi.notify import SendNotifications
from check_phat_nguoi.print_console import PrintConsole
from check_phat_nguoi.utils import setup_logger

logger = getLogger(__name__)


async def async_main() -> None:
    setup_logger()
    logger.debug(f"Config read: {config}")
    await GetData().get_data()
    logger.debug(f"Data got: {plates_context.plates}")
    PrintConsole().print_console()
    await SendNotifications().send()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
