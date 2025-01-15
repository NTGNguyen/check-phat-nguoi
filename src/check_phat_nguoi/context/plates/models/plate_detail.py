from __future__ import annotations

from typing import Any, override

from pydantic import BaseModel, Field

from check_phat_nguoi.types import VehicleTypeEnum, get_vehicle_enum

from .violation_detail import ViolationDetail


class PlateDetail(BaseModel):
    plate: str
    owner: str | None
    type: VehicleTypeEnum
    violations: tuple[ViolationDetail, ...] | None = Field(
        description="Danh sách các vi phạm của 1 biển xe",
    )

    @override
    def __hash__(self):
        return (
            hash(self.plate)
            + hash(self.owner)
            + hash(self.type)
            + hash(self.violations)
        )

    @override
    def __eq__(self, other: Any):
        if isinstance(other, PlateDetail):
            return (
                self.plate == other.plate
                and self.owner == other.owner
                and get_vehicle_enum(self.type) == get_vehicle_enum(other.type)
                and (
                    all(x == y for x, y in zip(self.violations, other.violations))
                    if self.violations and other.violations
                    else (not self.violations and not other.violations)
                )
            )
        return False

    # TODO: Handle show details later when main updates that option
    @override
    def __str__(self) -> str:
        plate_detail: str = f"Biển số: {self.plate}" + (
            f"\nChủ sở hữu: {self.owner}" if self.owner else ""
        )
        if self.violations:
            return (
                plate_detail
                + "\n"
                + "\n".join(
                    f"Lỗi vi phạm #{order}:\n{violation}\n"
                    for order, violation in enumerate(self.violations, start=1)
                )
            )
        else:
            return plate_detail


__all__ = ["PlateDetail"]
