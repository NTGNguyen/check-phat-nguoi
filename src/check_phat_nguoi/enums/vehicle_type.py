from enum import IntEnum


# TODO: Should we change this to string enum? Then make the function to convert to number
class VehicleTypeEnum(IntEnum):
    car = 1
    motorbike = 2
    electric_motorbike = 3


__all__ = ["VehicleTypeEnum"]
