from typing import LiteralString

CONFIG_PATHS: tuple[LiteralString, ...] = (
    "config.json",
    "check-phat-nguoi.config.json",
    "~/check-phat-nguoi.config.json",
)
SIMPLE_LOG_MESSAGE: LiteralString = "[%(levelname)s]: %(message)s"
DETAIL_LOG_MESSAGE: LiteralString = (
    "%(asctime)s [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d - %(pathname)s)"
)
