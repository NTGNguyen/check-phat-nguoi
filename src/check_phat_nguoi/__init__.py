from check_phat_nguoi.modules.config_reader import config
from check_phat_nguoi.modules.logger import setup_logger


def main() -> None:
    setup_logger()
    print(config)


__all__ = ["main"]
