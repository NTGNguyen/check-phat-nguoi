from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from check_phat_nguoi.types import LogLevelType

from .api import ApiEnum
from .notifications import TelegramNotificationDTO
from .plate_info import PlateInfoDTO


class ConfigDTO(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        alias_generator=to_camel,
    )

    plates: tuple[PlateInfoDTO, ...] = Field(
        description="Danh sách các biển xe",
        frozen=True,
    )
    notifications: tuple[TelegramNotificationDTO, ...] = Field(
        description="Danh sách các thiết lập để thông báo",
        frozen=True,
    )
    api: ApiEnum = Field(
        description="Sử dụng API từ trang web nào (mặc định sử dụng API từ trang checkphatnguoi.vn)",
        title="API",
        default=ApiEnum.checkphatnguoi_vn,
        frozen=True,
    )
    unpaid_only: bool = Field(
        description="Chỉ hiển thị thông tin vi phạm chưa nộp phạt",
        default=True,
        frozen=True,
    )
    verbose: bool = Field(
        description="Hiển thị tất cả thông tin có thể hiển thị",
        default=False,
        frozen=True,
    )
    request_timeout: int = Field(
        description="Thời gian (s) để gửi request đến server API và gửi notify message",
        default=10,
        frozen=True,
    )
    detail_log: bool = True
    log_level: LogLevelType = "WARNING"


__all__ = ["ConfigDTO"]
