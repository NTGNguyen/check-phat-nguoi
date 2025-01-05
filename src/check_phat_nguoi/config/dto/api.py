from enum import Enum


class ApiEnum(str, Enum):
    checkphatnguoi_vn = "checkphatnguoi.vn"
    csgt_vn = "csgt.vn"


__all__ = ["ApiEnum"]
