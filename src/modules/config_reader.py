from yaml import safe_load

from src.types.config import Config


def get_config(file):
    with open(file, "r", encoding="utf8") as file:
        data = safe_load(file)
        list_bien_so = [item["bien-so"] for item in data["data"]]
        for item in list_bien_so:
            print(item)


__all__ = ["get_config"]
