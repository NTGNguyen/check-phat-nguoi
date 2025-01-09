from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from check_phat_nguoi.types import ApiEnum, LogLevelType

from .notifications import TelegramNotificationConfig
from .plate_info import PlateInfo


class Config(BaseModel):
    model_config = ConfigDict(
        title="Config",
        use_enum_values=True,
        alias_generator=to_camel,
    )

    plates: tuple[PlateInfo, ...] = Field(
        title="Danh sách biển xe",
        description="Danh sách các biển xe",
        frozen=True,
    )
    notifications: tuple[TelegramNotificationConfig, ...] | None = Field(
        title="Danh sách thông báo",
        description="Danh sách các thiết lập để thông báo",
        frozen=True,
        default=None,
    )
    api: ApiEnum = Field(
        title="API",
        description="Sử dụng API từ trang web nào (mặc định sử dụng API từ trang checkphatnguoi.vn)",
        default=ApiEnum.checkphatnguoi_vn,
        frozen=True,
    )
    unpaid_only: bool = Field(
        title="Lọc chưa nộp phạt",
        description="Chỉ lọc các thông tin vi phạm chưa nộp phạt",
        default=True,
        frozen=True,
    )
    verbose: bool = Field(
        title="Hiển thị đầy đủ thông tin",
        description="Hiển thị tất cả thông tin có thể hiển thị",
        default=False,
        frozen=True,
    )
    request_timeout: int = Field(
        title="Thời gian request",
        description="Thời gian (s) để gửi request đến server API và gửi notify message",
        default=10,
        frozen=True,
    )
    request_per_time: int = Field(
        title="Số lượng request",
        description="Số lượng request tối chạy song song",
        default=5,
        frozen=True,
        gt=0,
    )
    detail_log: bool = Field(
        title="Log chi tiết",
        description="Log chi tiết",
        default=False,
        frozen=True,
    )
    log_level: LogLevelType = Field(
        title="Mức độ log",
        description="Mức độ log",
        default="WARNING",
        frozen=True,
    )


__all__ = ["Config"]
