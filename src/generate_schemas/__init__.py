from generate_schemas.modules import generate_config_schema


def main() -> None:
    generate_config_schema()


__all__ = ["generate_config_schema"]
