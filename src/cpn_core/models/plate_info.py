from typing import Any, override

from pydantic import BaseModel, ConfigDict, Field

from cpn_core.types.api import ApiEnum
from cpn_core.types.vehicle_type import (
    VehicleType,
    get_vehicle_enum,
    get_vehicle_str_vie,
)


class PlateInfo(BaseModel):
    model_config = ConfigDict(
        title="Thông tin biển số",
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
    apis: tuple[ApiEnum, ...] | None = Field(
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

    def get_str(self, *, show_less_detail: bool, markdown: bool) -> str:
        if markdown:
            return self._get_markdown_message(show_less_detail)
        else:
            return self._get_raw_messages(show_less_detail)

    def _get_raw_messages(self, show_less_detail: bool) -> str:
        message: str
        if show_less_detail:
            message = (
                (f"Biển số: {self.plate}")
                + (f"\nChủ sở hữu: {self.owner}" if self.owner else "")
            ).strip()
        else:
            message = (
                (f"Biển số: {self.plate}")
                + (f"\nChủ sở hữu: {self.owner}" if self.owner else "")
                + (f"\nLoại phương tiện: {get_vehicle_str_vie(self.type)}")
            ).strip()
        return "Thông tin phương tiện:\n" + message

    def _get_markdown_message(self, show_less_detail: bool) -> str:
        message: str
        if show_less_detail:
            message = (
                (f"*Biển số:* {self.plate}")
                + (f"\n*Chủ sở hữu:* {self.owner}" if self.owner else "")
            ).strip()
        else:
            message = (
                (f"*Biển số:* {self.plate}")
                + (f"\n*Chủ sở hữu:* {self.owner}" if self.owner else "")
                + (f"\n*Loại phương tiện:* {get_vehicle_str_vie(self.type)}")
            ).strip()
        return "*🚗 **Thông tin phương tiện**:*\n" + message

    @override
    def __hash__(self) -> int:
        return (
            hash(self.plate)
            + hash(self.type)
            + hash(self.enabled)
            + hash(self.apis)
            + hash(self.owner)
        )

    @override
    def __eq__(self, other: Any):
        if isinstance(other, PlateInfo):
            return (
                self.plate == other.plate
                and get_vehicle_enum(self.type) == get_vehicle_enum(other.type)
                and self.enabled == other.enabled
                and self.owner == other.owner
                and (
                    all(
                        x == y
                        for x, y in zip(
                            (self.apis,)
                            if isinstance(self.apis, ApiEnum)
                            else self.apis,
                            (other.apis,)
                            if isinstance(other.apis, ApiEnum)
                            else other.apis,
                        )
                    )
                    if self.apis and other.apis
                    else (not self.apis and not other.apis)
                )
            )
        return False


__all__ = ["PlateInfo"]
