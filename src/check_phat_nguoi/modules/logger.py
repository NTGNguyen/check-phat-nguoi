from logging import basicConfig

from check_phat_nguoi.modules.config_reader import config


def setup_logger() -> None:
    basicConfig(
        level=config.log_level,
        format="%(asctime)s [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)d)",
    )


__all__ = ["setup_logger"]
