from pydantic import BaseModel, ConfigDict

from check_phat_nguoi.models.log_level import LogLevelModel
from check_phat_nguoi.models.notify.telegram_notify import TelegramNotifyModel
from check_phat_nguoi.models.plate_info import PlateInfoModel


class ConfigModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    data: list[PlateInfoModel] = []
    notify: list[TelegramNotifyModel] = []
    havent_paid_only: bool = True
    detail_log: bool = False
    log_level: LogLevelModel = LogLevelModel.warning


print("coo")


__all__ = ["ConfigModel"]
