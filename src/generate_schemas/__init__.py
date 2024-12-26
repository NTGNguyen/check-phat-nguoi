from generate_schemas.modules import generate_config_schema


def main() -> None:
    print("Generating config schema...")
    generate_config_schema()


__all__ = ["generate_config_schema"]
