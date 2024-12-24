from enum import Enum


class LogLevelModel(str, Enum):
    notset = "NOTSET"
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


__all__ = ["LogLevelModel"]
