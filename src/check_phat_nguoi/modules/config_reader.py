from json import load

from check_phat_nguoi.models.config import Config


def config_reader(config_path) -> Config:
    with open(config_path, "r", encoding="utf8") as config:
        data = load(config)
        return Config(**data)
