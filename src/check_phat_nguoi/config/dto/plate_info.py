from __future__ import annotations

from typing import Any, override

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from check_phat_nguoi.types import (
    VehicleStrType,
)
from check_phat_nguoi.types.vehicle_type import VehicleTypeEnum

from .api import ApiEnum


class PlateInfoDTO(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )

    plate: str = Field(
        description="Biển số",
        title="Biển số",
        examples=["60A64685", "98-A-56604", "30-F88251", "59XB-00000"],
    )
    owner: str | None = Field(
        description="Ghi chú chủ sở hữu (phù hợp khi dùng notify ai đó)",
        title="Ghi chú chủ sở hữu",
        examples=["@kevinnitro", "dad"],
        default=None,
    )
    type: VehicleStrType | VehicleTypeEnum = Field(
        description="Loại phương tiện để gửi request cũng như lọc loại phương tiện đối với các API không lọc loại phương tiện sẵn",
        title="Loại phương tiện",
    )
    api: ApiEnum | None = Field(
        description="Sử dụng API từ trang web nào (để trống sẽ sử dụng API define ở scope ngoài)",
        title="API",
        default=None,
    )

    @override
    def __hash__(self):
        return hash(self.plate)

    @override
    def __eq__(self, other: Any):
        if isinstance(other, PlateInfoDTO):
            return self.plate == other.plate
        return False


__all__ = ["PlateInfoDTO"]
