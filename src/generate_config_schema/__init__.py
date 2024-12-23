from json import dumps

from pydantic import TypeAdapter

from check_phat_nguoi.models.config import Config


def main():
    adapter = TypeAdapter(Config)
    with open("schemas/config.json", "w", encoding="utf8") as file:
        file.write(dumps(adapter.json_schema(), indent=2))
