from pydantic import BaseModel, Field

from .violation import ViolationModel


class PlateInfoModel(BaseModel):
    plate: str
    owner: str | None
    violation: tuple[ViolationModel, ...] = Field(
        description="Danh sách các vi phạm của 1 biển xe", default_factory=tuple
    )


__all__ = ["PlateInfoModel"]
