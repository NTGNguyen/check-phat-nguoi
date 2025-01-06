from logging import basicConfig

from check_phat_nguoi.constants.config import (
    DETAIL_LOG_MESSAGE,
    SIMPLE_LOG_MESSAGE,
)
from check_phat_nguoi.context.config.config_reader import config


def setup_logger() -> None:
    basicConfig(
        level=config.log_level,
        format=DETAIL_LOG_MESSAGE if config.detail_log else SIMPLE_LOG_MESSAGE,
    )


__all__ = ["setup_logger"]
