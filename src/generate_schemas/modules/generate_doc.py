from json_schema_for_humans.generate import generate_from_filename
from json_schema_for_humans.generation_configuration import GenerationConfiguration

from ..utils.constants import CONFIG_SCHEMA_PATH, GENERATE_SCHEMAS_WEBSITES_PATH


def generate_doc():
    config: GenerationConfiguration = GenerationConfiguration(
        copy_css=True, expand_buttons=True
    )

    generate_from_filename(
        CONFIG_SCHEMA_PATH, GENERATE_SCHEMAS_WEBSITES_PATH, config=config
    )


if __name__ == "__main__":
    generate_doc()
