from pydantic import BaseModel, Field

from .plate_info import PlateInfoModel


class PlatesModel(BaseModel):
    plates: list[PlateInfoModel] = Field(
        description="Danh sách các biển xe", default_factory=list
    )


__all__ = ["PlatesModel"]
