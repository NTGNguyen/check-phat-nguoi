from pydantic import BaseModel, ConfigDict

from check_phat_nguoi.models.config.log_level import LogLevelModel
from check_phat_nguoi.models.config.notify.telegram_notify import TelegramNotifyModel
from check_phat_nguoi.models.config.plate_info import PlateInfoModel


class ConfigModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    data: list[PlateInfoModel] = []
    notify: list[TelegramNotifyModel] = []
    havent_paid_only: bool = True
    detail_log: bool = False
    log_level: LogLevelModel = LogLevelModel.warning


__all__ = ["ConfigModel"]
