from check_phat_nguoi.models.context.plate_context.violation import (
    ViolationContextModel,
)
from check_phat_nguoi.models.plate_info import PlateInfoModel


class PlateInfoContextModel(PlateInfoModel):
    violation: list[ViolationContextModel] = []


__all__ = ["PlateInfoContextModel"]
