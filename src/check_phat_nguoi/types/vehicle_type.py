from __future__ import annotations

from enum import IntEnum
from typing import Any, Literal, TypeAlias, Union


class VehicleTypeEnum(IntEnum):
    car = 1
    motorbike = 2
    electric_motorbike = 3


VehicleStrType: TypeAlias = Literal["car", "motorbike", "electric_motorbike"]

VehicleIntType: TypeAlias = Literal[1, 2, 3]

VehicleType: TypeAlias = Union[VehicleIntType, VehicleStrType]


def get_vehicle_enum(type: VehicleTypeEnum | VehicleType | Any) -> VehicleTypeEnum:
    if isinstance(type, VehicleTypeEnum):
        return type
    match type:
        case "car" | 1:
            return VehicleTypeEnum.car
        case "motorbike" | 2:
            return VehicleTypeEnum.motorbike
        case "electric_motorbike" | 3:
            return VehicleTypeEnum.electric_motorbike
        case _:
            raise ValueError("Unknown vehicle type")


__all__ = [
    "VehicleIntType",
    "VehicleStrType",
    "VehicleType",
    "VehicleTypeEnum",
    "get_vehicle_enum",
]
