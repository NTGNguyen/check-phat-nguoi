from json import load
from os.path import exists as path_exists
from typing import Final

from pydantic import ValidationError

from cpn_cli.constants import CONFIG_PATHS
from cpn_cli.models.config import Config


def _config_reader() -> Config:
    for config_path in CONFIG_PATHS:
        if path_exists(config_path):
            try:
                with open(config_path, encoding="utf8") as config:
                    data = load(config)
                    return Config(**data)
            except ValidationError as e:
                print("Failed to read the config!")
                print(e)
                exit(1)
    print("No config was found!")
    exit(1)


config: Final[Config] = _config_reader()
