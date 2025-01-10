from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from check_phat_nguoi.types import ApiEnum, LogLevelType

from .notifications.base_notification import (
    BaseNotificationConfig,
)
from .plate_info import PlateInfo


class Config(BaseModel):
    model_config = ConfigDict(
        title="Config",
        use_enum_values=True,
        frozen=True,
    )

    plates_infos: tuple[PlateInfo, ...] = Field(
        title="Danh sách biển xe",
        description="Danh sách các biển xe",
        min_length=1,
    )
    notifications: tuple[BaseNotificationConfig, ...] = Field(
        title="Danh sách thông báo",
        description="Danh sách các thiết lập để thông báo",
        default_factory=tuple,
    )
    api: tuple[ApiEnum, ...] | ApiEnum = Field(
        title="API",
        description="Sử dụng API từ trang web nào. Mặc định sẽ là list các API và dừng khi 1 API lấy dữ liệu thành công. Có thể điền giá trị trùng để retry. Hoặc chỉ dùng 1 API.",
        default=(ApiEnum.checkphatnguoi_vn, ApiEnum.csgt_vn),
        min_length=1,
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
