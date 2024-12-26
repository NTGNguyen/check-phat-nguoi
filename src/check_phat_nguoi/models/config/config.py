from pydantic import BaseModel, ConfigDict, Field

from check_phat_nguoi.models.log_level import LogLevelModel
from check_phat_nguoi.models.notify.telegram_notify import TelegramNotifyModel
from check_phat_nguoi.models.plate_info import PlateInfoModel


class ConfigModel(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    data: list[PlateInfoModel] = Field(
        description="Danh sách các biển xe", default_factory=list
    )
    notify: list[TelegramNotifyModel] = Field(
        description="Danh sách các thiết lập để thông báo", default_factory=list
    )
    unpaid_only: bool = Field(
        description="Chỉ hiển thị thông tin vi phạm chưa nộp phạt", default=True
    )
    verbose: bool = Field(
        description="Hiển thị tất cả thông tin có thể hiển thị", default=False
    )
    detail_log: bool = True
    log_level: LogLevelModel = LogLevelModel.info


__all__ = ["ConfigModel"]
