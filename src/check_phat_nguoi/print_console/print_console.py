from logging import getLogger

from check_phat_nguoi.config_reader import config
from check_phat_nguoi.context import PlateDetail, plates_context

logger = getLogger(__name__)


class PrintConsole:
    def __init__(self):
        self.plate_details: tuple[PlateDetail, ...] = plates_context.plates

    def print_console(self) -> None:
        if not config.print_console:
            return
        if not self.plate_details:
            logger.info("No plate details. Skip printing")
            return
        for plate_detail in self.plate_details:
            print(plate_detail)
