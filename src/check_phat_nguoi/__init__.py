from logging import Logger, getLogger

from check_phat_nguoi.modules.config_reader import config
from check_phat_nguoi.modules.logger import setup_logger

logger: Logger = getLogger(__name__)


def main() -> None:
    setup_logger()
    logger.debug(config)


__all__ = ["main"]
