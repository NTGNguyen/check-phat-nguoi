from logging import getLogger

from cpn_cli.models.plate_detail import PlateDetail
from cpn_cli.modules.config_reader import config

logger = getLogger(__name__)


class PrintConsole:
    def __init__(self, plate_details: tuple[PlateDetail, ...]) -> None:
        self.plate_details: tuple[PlateDetail, ...] = plate_details

    def print_console(self) -> None:
        if not config.print_console:
            return
        if not self.plate_details:
            logger.info("No plate details. Skip printing")
            return
        # HACK: Have to convert each plate detail to str to use join method :v
        print(
            "\n\n---\n\n".join(str(plate_detail) for plate_detail in self.plate_details)
        )
