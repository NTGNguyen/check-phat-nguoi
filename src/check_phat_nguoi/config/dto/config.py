from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from .api import ApiEnum
from .notify.telegram_notify import TelegramNotifyDTO
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
    notifications: tuple[TelegramNotifyDTO, ...] = Field(
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
        description="Thời gian (s) để gửi request đến server API và gửi message notify",
        default=10,
        frozen=True,
    )
    detail_log: bool = True
    log_level: Literal[
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "WARNING"


__all__ = ["ConfigDTO"]
