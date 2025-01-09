from json import load
from os.path import exists as path_exists
from typing import Final

from pydantic import ValidationError

from check_phat_nguoi.constants.config import CONFIG_PATHS

from .config.dto import ConfigDTO
from .config.exceptions import NoConfigFoundException


def _config_reader() -> ConfigDTO:
    for config_path in CONFIG_PATHS:
        if path_exists(config_path):
            try:
                with open(config_path, encoding="utf8") as config:
                    data = load(config)
                    return ConfigDTO(**data)
            except ValidationError as e:
                print("Failed to read the config!")
                print(e)
                exit(1)

    raise NoConfigFoundException()


config: Final[ConfigDTO] = _config_reader()


__all__ = ["config"]
