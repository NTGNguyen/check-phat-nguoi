from __future__ import annotations

from typing import Any, override

from pydantic import BaseModel, Field

from check_phat_nguoi.types import VehicleTypeEnum

from .violation import ViolationModel


class PlateInfoModel(BaseModel):
    plate: str
    owner: str | None
    type: VehicleTypeEnum
    violation: tuple[ViolationModel, ...] = Field(
        description="Danh sách các vi phạm của 1 biển xe",
    )

    @override
    def __hash__(self):
        return hash(self.plate)

    @override
    def __eq__(self, other: Any):
        if isinstance(other, PlateInfoModel):
            return self.plate == other.plate
        return False


__all__ = ["PlateInfoModel"]
