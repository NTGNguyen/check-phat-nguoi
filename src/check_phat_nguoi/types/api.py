from enum import Enum


class ApiEnum(str, Enum):
    checkphatnguoi_vn = "checkphatnguoi.vn"
    csgt_vn = "csgt.vn"
    phatnguoi_vn = "phatnguoi.vn"
    etraffic_gtelict_vn = "etraffic.gtelict.vn"


__all__ = ["ApiEnum"]
