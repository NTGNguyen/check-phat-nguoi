from pydantic import Field

from check_phat_nguoi.models.context.plate_context.violation import (
    ViolationContextModel,
)
from check_phat_nguoi.models.plate_info import PlateInfoModel


class PlateInfoContextModel(PlateInfoModel):
    violation: list[ViolationContextModel] = Field(
        description="Danh sách các vi phạm của 1 biển xe", default_factory=list
    )


__all__ = ["PlateInfoContextModel"]
