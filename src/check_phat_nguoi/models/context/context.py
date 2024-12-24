from pydantic import BaseModel

from check_phat_nguoi.models.context.plate_info import PlateInfoModel


class ContextModel(BaseModel):
    data: list[PlateInfoModel] = []


__all__ = ["ContextModel"]
