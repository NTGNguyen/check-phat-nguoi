from json import load
from os.path import exists as path_exists
from typing import Final

from check_phat_nguoi.config.exceptions.no_config_found import NoConfigFoundException
from check_phat_nguoi.modules.constants.config import CONFIG_PATHS

from .dto import ConfigDTO


def _config_reader() -> ConfigDTO:
    for config_path in CONFIG_PATHS:
        if path_exists(config_path):
            with open(config_path, "r", encoding="utf8") as config:
                data = load(config)
                return ConfigDTO(**data)
    raise NoConfigFoundException()


config: Final[ConfigDTO] = _config_reader()


__all__ = ["config"]
