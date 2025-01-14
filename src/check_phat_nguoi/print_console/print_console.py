from asyncio import gather
from logging import getLogger
from sys import stdout

from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.context import PlateDetail, plates_context

logger = getLogger(__name__)


class PrintConsole:
    def __init__(self):
        self.plate_details: tuple[PlateDetail, ...]

    @staticmethod
    async def async_print(plate_detail: PlateDetail):
        stdout.write(str(plate_detail))
        stdout.flush()

    async def print_console(self):
        self.plate_details = plates_context.plates
        if self.plate_details == ():
            logger.debug("No plate details. Skip printing")
            return
        if config.print_console:
            await gather(
                *(
                    PrintConsole.async_print(plate_detail)
                    for plate_detail in self.plate_details
                )
            )
