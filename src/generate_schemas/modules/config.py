from json import dumps

from pydantic import TypeAdapter

from check_phat_nguoi.models.config import ConfigModel
from generate_schemas.utils.constant import CONFIG_SCHEMA_PATH


def generate_config_schema():
    adapter = TypeAdapter(ConfigModel)
    with open(CONFIG_SCHEMA_PATH, "w", encoding="utf8") as file:
        file.write(dumps(adapter.json_schema(), indent=2))
    print(f"Created {CONFIG_SCHEMA_PATH} successfully!")
