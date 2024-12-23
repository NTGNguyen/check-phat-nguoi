from pydantic import BaseModel, ConfigDict

from check_phat_nguoi.models.log_level import LogLevel
from check_phat_nguoi.models.notify.telegram_notify import TelegramNotify
from check_phat_nguoi.models.plate_info import PlateInfo


class Config(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    data: list[PlateInfo] = []
    notify: list[TelegramNotify] = []
    havent_paid_only: bool = True
    detail_log: bool = False
    log_level: LogLevel = LogLevel.warning


__all__ = ["Config"]
