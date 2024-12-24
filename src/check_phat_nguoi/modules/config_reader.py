from json import load

from check_phat_nguoi.models.config import ConfigModel
from check_phat_nguoi.utils.constants import CONFIG_PATH


def _config_reader(config_path: str) -> ConfigModel:
    with open(config_path, "r", encoding="utf8") as config:
        data = load(config)
        return ConfigModel(**data)


config: ConfigModel = _config_reader(CONFIG_PATH)

__all__ = ["config"]
