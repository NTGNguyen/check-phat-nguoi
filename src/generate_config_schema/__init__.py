from json import dumps

from pydantic import TypeAdapter

from check_phat_nguoi.models.config import ConfigModel


def main():
    adapter = TypeAdapter(ConfigModel)
    with open("schemas/config.json", "w", encoding="utf8") as file:
        file.write(dumps(adapter.json_schema(), indent=2))
