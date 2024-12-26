from pydantic import BaseModel, Field

from check_phat_nguoi.models.context.plate_context.plate_info import (
    PlateInfoContextModel,
)


class PlatesContextModel(BaseModel):
    plates: list[PlateInfoContextModel] = Field(
        description="Danh sách các biển xe", default_factory=list
    )


__all__ = ["PlatesContextModel"]
