from pydantic import BaseModel, Field

from check_phat_nguoi.enums import VehicleTypeEnum

from .violation import ViolationModel


class PlateInfoModel(BaseModel):
    plate: str
    owner: str | None
    type: VehicleTypeEnum | None
    violation: tuple[ViolationModel, ...] = Field(
        description="Danh sách các vi phạm của 1 biển xe", default_factory=tuple
    )


__all__ = ["PlateInfoModel"]
