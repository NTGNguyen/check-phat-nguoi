from json import load

from ..models.config import Config


def config_reader(config_path) -> Config:
    with open(config_path, "r", encoding="utf8") as config:
        data = load(config)
        return Config(**data)
