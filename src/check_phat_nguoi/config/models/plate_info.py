from __future__ import annotations

from typing import Any, override

from pydantic import BaseModel, ConfigDict, Field

from check_phat_nguoi.types import (
    ApiEnum,
    VehicleType,
)


class PlateInfo(BaseModel):
    model_config = ConfigDict(
        title="Thông tin thiết lập cho biển số",
        frozen=True,
    )

    plate: str = Field(
        description="Biển số",
        title="Biển số",
        examples=["60A64685", "98-A-56604", "30-F88251", "59XB-00000"],
    )
    type: VehicleType = Field(
        description="Loại phương tiện để gửi request cũng như lọc loại phương tiện đối với các API không lọc loại phương tiện sẵn",
        title="Loại phương tiện",
    )
    enabled: bool = Field(
        description="Kích hoạt",
        default=True,
    )
    api: tuple[ApiEnum, ...] | ApiEnum | None = Field(
        description='Sử dụng API từ trang web nào. Config giống "api" ở ngoài .Để trống sẽ sử dụng API define ở scope ngoài.',
        title="API",
        default=None,
        min_length=1,
    )
    owner: str | None = Field(
        description="Ghi chú chủ sở hữu (phù hợp khi dùng nhắc ai đó với lựa chọn notifications)",
        title="Ghi chú chủ sở hữu",
        examples=["@kevinnitro", "dad"],
        default=None,
    )

    @override
    def __hash__(self):
        return hash(self.plate)

    @override
    def __eq__(self, other: Any):
        if isinstance(other, PlateInfo):
            return self.plate == other.plate
        return False


__all__ = ["PlateInfo"]
