import asyncio
from logging import getLogger

from cpn_cli.config_reader import config
from cpn_cli.get_data import GetData
from cpn_cli.models import PlateDetail
from cpn_cli.notify import Notify
from cpn_cli.print_console import PrintConsole
from cpn_cli.setup_logger import setup_logger

logger = getLogger(__name__)


async def async_main() -> None:
    setup_logger()
    logger.debug(f"Config read: {config}")
    plate_details: tuple[PlateDetail, ...] = await GetData().get_data()
    PrintConsole(plate_details=plate_details).print_console()
    await Notify(plate_details=plate_details).send()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
