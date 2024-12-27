from pydantic import BaseModel, ConfigDict, Field

from .log_level import LogLevelDTO
from .notify.telegram_notify import TelegramNotifyDTO
from .plate_info import PlateInfoDTO


class ConfigDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_desfault=True)

    data: tuple[PlateInfoDTO, ...] = Field(
        description="Danh sách các biển xe", default_factory=tuple
    )
    notify: tuple[TelegramNotifyDTO, ...] = Field(
        description="Danh sách các thiết lập để thông báo", default_factory=tuple
    )
    unpaid_only: bool = Field(
        description="Chỉ hiển thị thông tin vi phạm chưa nộp phạt", default=True
    )
    verbose: bool = Field(
        description="Hiển thị tất cả thông tin có thể hiển thị", default=False
    )
    detail_log: bool = True
    log_level: LogLevelDTO = LogLevelDTO.info


__all__ = ["ConfigDTO"]
