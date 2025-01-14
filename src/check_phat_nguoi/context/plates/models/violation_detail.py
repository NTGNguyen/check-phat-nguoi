from __future__ import annotations

from datetime import datetime
from typing import override

from pydantic import BaseModel, Field


# NOTE: This class is used to store the get data's reponse. So it has None type in each field
class ViolationDetail(BaseModel):
    color: str | None = Field(
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
    resolution_offices_details: tuple[str, ...] | None = Field(
        description="Nơi giải quyết vụ việc",
        default=None,
    )

    @override
    def __hash__(self):
        return hash(self.date) + hash(self.location)
