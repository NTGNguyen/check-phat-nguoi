from enum import IntEnum
from typing import Any, Literal, TypeAlias


class VehicleTypeEnum(IntEnum):
    car = 1
    motorbike = 2
    electric_motorbike = 3


VehicleStrType: TypeAlias = Literal["car", "motorbike", "electric_motorbike"]


def get_vehicle_enum(type: Any) -> VehicleTypeEnum:
    if isinstance(type, VehicleTypeEnum):
        return type
    match type:
        case "car":
            return VehicleTypeEnum.car
        case "motorbike":
            return VehicleTypeEnum.motorbike
        case "electric_motorbike":
            return VehicleTypeEnum.electric_motorbike
        case _:
            raise ValueError("Unknown vehicle type")


__all__ = ["VehicleTypeEnum", "VehicleStrType", "get_vehicle_enum"]
