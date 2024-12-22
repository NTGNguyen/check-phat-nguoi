from .modules.config_reader import config_reader


def main():
    print(config_reader("config.yml"))
