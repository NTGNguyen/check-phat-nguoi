from enum import IntEnum
from typing import Any, Literal, TypeAlias


class VehicleTypeEnum(IntEnum):
    car = 1
    motorbike = 2
    electric_motorbike = 3


VehicleStrVieType: TypeAlias = Literal["Ô tô", "Xe máy", "Xe máy điện"]

VehicleStrType: TypeAlias = Literal["car", "motorbike", "electric_motorbike"]

VehicleIntType: TypeAlias = Literal[1, 2, 3]

VehicleType: TypeAlias = VehicleIntType | VehicleStrType | VehicleStrVieType


def get_vehicle_enum(type: VehicleTypeEnum | VehicleType | Any) -> VehicleTypeEnum:
    if isinstance(type, VehicleTypeEnum):
        return type
    match type:
        case "car" | "Ô tô" | 1 | VehicleTypeEnum.car:
            return VehicleTypeEnum.car
        case "motorbike" | "Xe máy" | 2 | VehicleTypeEnum.motorbike:
            return VehicleTypeEnum.motorbike
        case (
            "electric_motorbike"
            | "Xe máy điện"
            | 3
            | VehicleTypeEnum.electric_motorbike
        ):
            return VehicleTypeEnum.electric_motorbike
        case _:
            raise ValueError("Unknown vehicle type")


def get_vehicle_str(type: VehicleTypeEnum | VehicleType | Any) -> VehicleStrType:
    match type:
        case "car" | "Ô tô" | 1 | VehicleTypeEnum.car:
            return "car"
        case "motorbike" | "Xe máy" | 2 | VehicleTypeEnum.motorbike:
            return "motorbike"
        case (
            "electric_motorbike"
            | "Xe máy điện"
            | 3
            | VehicleTypeEnum.electric_motorbike
        ):
            return "electric_motorbike"
        case _:
            raise ValueError("Unknown vehicle type")


def get_vehicle_str_vie(type: VehicleTypeEnum | VehicleType | Any) -> VehicleStrVieType:
    match type:
        case "car" | "Ô tô" | 1 | VehicleTypeEnum.car:
            return "Ô tô"
        case "motorbike" | "Xe máy" | 2 | VehicleTypeEnum.motorbike:
            return "Xe máy"
        case (
            "electric_motorbike"
            | "Xe máy điện"
            | 3
            | VehicleTypeEnum.electric_motorbike
        ):
            return "Xe máy điện"
        case _:
            raise ValueError("Unknown vehicle type")


__all__ = [
    "VehicleIntType",
    "VehicleStrType",
    "VehicleStrVieType",
    "VehicleType",
    "VehicleTypeEnum",
    "get_vehicle_enum",
    "get_vehicle_str",
]
