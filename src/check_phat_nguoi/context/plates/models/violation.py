from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .resolution_office import ResolutionOffice


class Violation(BaseModel):
    type: Literal["Ô tô", "Xe máy", "Xe đạp điện"] | None = Field(
        description="Loại phương tiện giao thông", default=None
    )
    date: datetime | None = Field(description="Thời điểm vi phạm", default=None)
    location: str | None = Field(description="Vị trí vi phạm", default=None)
    action: str | None = Field(description="Hành vi vi phạm", default=None)
    status: bool | None = Field(
        description="Đã nộp phạt (True) / Chưa nộp phạt (False)", default=None
    )
    enforcement_unit: str | None = Field(
        description="Đơn vị phát hiện vi phạm", default=None
    )
    resolution_office: tuple[ResolutionOffice, ...] | None = Field(
        description="Nơi giải quyết vụ việc", default=None
    )
