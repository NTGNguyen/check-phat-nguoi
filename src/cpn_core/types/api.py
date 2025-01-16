from enum import Enum


class ApiEnum(str, Enum):
    checkphatnguoi_vn = "checkphatnguoi.vn"
    csgt_vn = "csgt.vn"
    phatnguoi_vn = "phatnguoi.vn"


__all__ = ["ApiEnum"]
