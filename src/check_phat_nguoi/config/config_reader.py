from json import load

from check_phat_nguoi.utils.constants import CONFIG_PATH

from .dto import ConfigDTO


def _config_reader(config_path: str) -> ConfigDTO:
    with open(config_path, "r", encoding="utf8") as config:
        data = load(config)
        return ConfigDTO(**data)


config: ConfigDTO = _config_reader(CONFIG_PATH)


__all__ = ["config"]
