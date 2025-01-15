from __future__ import annotations

from datetime import datetime
from typing import override

from pydantic import BaseModel, ConfigDict, Field

from check_phat_nguoi.types import VehicleTypeEnum, get_vehicle_str_vie


# NOTE: This class is used to store the get data's reponse. So it has None type in each field
class ViolationDetail(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )

    plate: str | None = Field(
        description="Biển định danh được trả về từ API",
        default=None,
    )
    color: str | None = Field(
        description="Màu biển",
        default=None,
    )
    type: VehicleTypeEnum | None = Field(
        description="Màu biển",
        default=None,
    )
    date: datetime | None = Field(
        description="Thời điểm vi phạm",
        default=None,
    )
    location: str | None = Field(
        description="Vị trí vi phạm",
        default=None,
    )
    violation: str | None = Field(
        description="Hành vi vi phạm",
        default=None,
    )
    status: bool | None = Field(
        description="Đã nộp phạt (True) / Chưa nộp phạt (False)",
        default=None,
    )
    enforcement_unit: str | None = Field(
        description="Đơn vị phát hiện vi phạm",
        default=None,
    )
    resolution_offices: tuple[str, ...] | None = Field(
        description="Nơi giải quyết vụ việc",
        default=None,
    )

    @override
    def __str__(self) -> str:
        return (
            (f"Biển: {self.plate}" if self.plate else "")
            + (f"\nMàu biển: {self.color}" if self.color else "")
            + (f"\nLoại xe: {get_vehicle_str_vie(self.type)}" if self.type else "")
            + (f"\nThời điểm vi phạm: {self.date}" if self.date else "")
            + (f"\nVị trí vi phạm: {self.location}" if self.location else "")
            + (f"\nHành vi vi phạm: {self.violation}" if self.violation else "")
            + (
                f"\nTrạng thái: {'Đã xử phạt' if self.status else 'Chưa xử phạt'}"
                if self.status
                else ""
            )
            + (
                f"\nĐơn vị phát hiện vi phạm: {self.enforcement_unit}"
                if self.enforcement_unit
                else ""
            )
            + (
                "\n" + "\n".join(self.resolution_offices)
                if self.resolution_offices
                else ""
            )
        ).strip()

    @override
    def __hash__(self):
        return (
            hash(self.plate) + hash(self.color) + hash(self.date) + hash(self.location)
        )
