from typing import Any, override

from pydantic import BaseModel, Field

from check_phat_nguoi.enums import VehicleTypeEnum

from .api import ApiEnum


class PlateInfoDTO(BaseModel):
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
    type: VehicleTypeEnum | None = Field(
        description='Loại phương tiện. Khi sử dụng API "checkphatnguoi_vn" không cần trường này',
        title="Loại phương tiện",
        default=None,
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
