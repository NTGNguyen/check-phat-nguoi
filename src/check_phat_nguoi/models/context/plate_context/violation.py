from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ViolationContextModel(BaseModel):
    type: Literal["Ô tô", "Xe máy", "Xe đạp điện"]
    date: datetime
    location: str
    action: str
    status: bool
    enforcement_unit: str | None = Field(
        description="Đơn vị phát hiện vi phạm", default=None
    )
    resolution_office: str | None = Field(
        description="Nơi giải quyết vụ việc", default=None
    )
