import asyncio
from logging import getLogger

from cpn_cli.models.plate_detail import PlateDetail
from cpn_cli.modules.config_reader import config
from cpn_cli.modules.get_data import GetData
from cpn_cli.modules.notify import Notify
from cpn_cli.modules.print_console import PrintConsole
from cpn_cli.modules.setup_logger import setup_logger

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
