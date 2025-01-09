from json import dumps

from pydantic import TypeAdapter

from check_phat_nguoi import Config
from generate_schemas.utils.constants import CONFIG_SCHEMA_PATH


def generate_config_schema():
    print("Generating config schema...")
    adapter: TypeAdapter[Config] = TypeAdapter(Config)
    with open(CONFIG_SCHEMA_PATH, "w", encoding="utf8") as file:
        file.write(dumps(adapter.json_schema(), indent=2, ensure_ascii=False))
    print(f"Created config schema successfully at {CONFIG_SCHEMA_PATH}!")
