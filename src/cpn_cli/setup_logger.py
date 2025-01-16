from logging import basicConfig

from cpn_cli.config_reader import config
from cpn_cli.constants import (
    DETAIL_LOG_MESSAGE,
    SIMPLE_LOG_MESSAGE,
)


def setup_logger() -> None:
    basicConfig(
        level=config.log_level.value,
        format=DETAIL_LOG_MESSAGE if config.detail_log else SIMPLE_LOG_MESSAGE,
    )


__all__ = ["setup_logger"]
