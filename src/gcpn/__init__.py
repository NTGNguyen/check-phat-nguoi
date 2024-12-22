from .modules.config_reader import get_config


def main():
    get_config("config.yml")
