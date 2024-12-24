from datetime import datetime

from pydantic import Field

from check_phat_nguoi.models.config.plate_info import PlateInfo as _PlateInfoConfig


class PlateInfo(_PlateInfoConfig):
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


__all__ = ["PlateInfo"]
