from json_schema_for_humans.generate import generate_from_filename
from json_schema_for_humans.generation_configuration import GenerationConfiguration


def generate_doc():
    config: GenerationConfiguration = GenerationConfiguration(
        copy_css=True, expand_buttons=True
    )

    generate_from_filename(
        "schemas/config.json", "sites/schemas/schema_doc.html", config=config
    )


if __name__ == "__main__":
    generate_doc()
