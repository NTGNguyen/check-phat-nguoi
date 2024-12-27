from enum import Enum


class LogLevelDTO(str, Enum):
    notset = "NOTSET"
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


__all__ = ["LogLevelDTO"]
