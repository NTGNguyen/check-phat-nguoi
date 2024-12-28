from pydantic import BaseModel, Field

from .plate_info import PlateInfoModel


class PlatesModel(BaseModel):
    plates: tuple[PlateInfoModel, ...] = Field(
        description="Danh sách các biển xe", default_factory=tuple
    )


__all__ = ["PlatesModel"]
