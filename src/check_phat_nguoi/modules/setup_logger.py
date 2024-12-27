from logging import basicConfig

from check_phat_nguoi.config import config
from check_phat_nguoi.utils.constants import DETAIL_LOG_MESSAGE, SIMPLE_LOG_MESSAGE


def setup_logger() -> None:
    basicConfig(
        level=config.log_level,
        format=DETAIL_LOG_MESSAGE if config.detail_log else SIMPLE_LOG_MESSAGE,
    )


__all__ = ["setup_logger"]
