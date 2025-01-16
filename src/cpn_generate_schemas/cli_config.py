from json import dumps
from os import makedirs
from os.path import dirname

from pydantic import TypeAdapter

from cpn_cli.models import Config

from .constants import CLI_CONFIG_SCHEMA_PATH


def generate_cli_config_schema():
    print("Generating config schema...")
    makedirs(dirname(CLI_CONFIG_SCHEMA_PATH), exist_ok=True)
    adapter: TypeAdapter[Config] = TypeAdapter(Config)
    with open(CLI_CONFIG_SCHEMA_PATH, "w", encoding="utf8") as file:
        file.write(dumps(adapter.json_schema(), indent=2, ensure_ascii=False))
    print(f"Created config schema successfully at {CLI_CONFIG_SCHEMA_PATH}!")
