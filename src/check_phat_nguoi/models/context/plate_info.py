from check_phat_nguoi.models.config.plate_info import (
    PlateInfoModel as _PlateInfoConfigModel,
)
from check_phat_nguoi.models.context.violation import ViolationModel


class PlateInfoModel(_PlateInfoConfigModel):
    violation: list[ViolationModel] = []


__all__ = ["PlateInfoModel"]
