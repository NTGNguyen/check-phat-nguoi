from pydantic import BaseModel

from check_phat_nguoi.models.context.plate_context.plate_info import (
    PlateInfoContextModel,
)


class PlatesContextModel(BaseModel):
    plates: list[PlateInfoContextModel] = []


__all__ = ["PlatesContextModel"]
