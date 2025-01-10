from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from check_phat_nguoi.types import ApiEnum, LogLevelType

from .notifications import TelegramNotificationConfig
from .plate_info import PlateInfo


class Config(BaseModel):
    model_config = ConfigDict(
        title="Config",
        use_enum_values=True,
        frozen=True,
    )

    plates: tuple[PlateInfo, ...] = Field(
        title="Danh sách biển xe",
        description="Danh sách các biển xe",
    )
    notifications: tuple[TelegramNotificationConfig, ...] | None = Field(
        title="Danh sách thông báo",
        description="Danh sách các thiết lập để thông báo",
        default=None,
    )
    api: ApiEnum = Field(
        title="API",
        description="Sử dụng API từ trang web nào (mặc định sử dụng API từ trang checkphatnguoi.vn)",
        default=ApiEnum.checkphatnguoi_vn,
    )
    pending_fines_only: bool = Field(
        title="Lọc chưa nộp phạt",
        description="Chỉ lọc các thông tin vi phạm chưa nộp phạt",
        default=True,
    )
    detail: bool = Field(
        title="Hiển thị đầy đủ thông tin",
        description="Hiển thị tất cả thông tin có thể hiển thị",
        default=False,
    )
    request_timeout: int = Field(
        title="Thời gian request",
        description="Thời gian (s) để gửi request đến server API và gửi notify message",
        default=10,
    )
    request_per_time: int = Field(
        title="Số lượng request",
        description="Số lượng request tối chạy song song",
        default=5,
        ge=0,
    )
    detail_log: bool = Field(
        title="Log chi tiết",
        description="Log chi tiết",
        default=False,
    )
    log_level: LogLevelType = Field(
        title="Mức độ log",
        description="Mức độ log",
        default="WARNING",
    )


__all__ = ["Config"]
