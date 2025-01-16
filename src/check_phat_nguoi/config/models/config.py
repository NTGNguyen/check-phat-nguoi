from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from check_phat_nguoi.types import ApiEnum
from check_phat_nguoi.types.log_level import LogLevelEnum

from .notifications import (
    DiscordNotificationConfig,
    TelegramNotificationConfig,
)
from .plate_info import PlateInfo


class Config(BaseModel):
    model_config = ConfigDict(
        title="Config",
        frozen=True,
    )

    plates_infos: tuple[PlateInfo, ...] = Field(
        title="Danh sách biển xe",
        description="Danh sách các biển xe",
        min_length=1,
    )
    # NOTE: Do not put base class in here. Because it will be wrong in schema.
    notifications: tuple[
        TelegramNotificationConfig | DiscordNotificationConfig, ...
    ] = Field(
        title="Danh sách thông báo",
        description="Danh sách các thiết lập để thông báo",
        default_factory=tuple,
    )
    apis: tuple[ApiEnum, ...] = Field(
        title="API",
        description="Sử dụng API từ trang web nào. Mặc định sẽ là list các API như trong schema hiển thị và dừng khi 1 API lấy dữ liệu thành công. Có thể điền giá trị trùng để retry. Hoặc chỉ dùng 1 API",
        default=(ApiEnum.phatnguoi_vn, ApiEnum.checkphatnguoi_vn),
        min_length=1,
    )
    print_console: bool = Field(
        title="In thông tin ra console",
        description="In thông tin của các biển ra console",
        default=True,
    )
    pending_fines_only: bool = Field(
        title="Lọc chưa nộp phạt",
        description="Chỉ lọc các thông tin vi phạm chưa nộp phạt",
        default=True,
    )
    show_less_details: bool = Field(
        title="Hiển thị ít thông tin",
        description="Chỉ hiển thị những thông tin biển vi phạm cần thiết",
        default=False,
    )
    request_timeout: int = Field(
        title="Thời gian request",
        description="Thời gian (s) để gửi request đến server API và gửi notify message",
        default=20,
    )
    asynchronous: bool = Field(
        title="Gửi và chờ tất cả request",
        description="Gửi và chờ tất cả request. Đối với API csgt.vn hãy tắt vì gửi request quá nhiều, trang lỗi. Nếu bật, các request sẽ không đảm bảo thứ tự input. Notify hiện không đảm bảo thứ tự input.",
        default=True,
    )
    detail_log: bool = Field(
        title="Log chi tiết",
        description="Log nhiều thông tin chi tiết hơn",
        default=False,
    )
    log_level: LogLevelEnum = Field(
        title="Mức độ log",
        description="Mức độ log",
        default=LogLevelEnum.warning,
    )


__all__ = ["Config"]
