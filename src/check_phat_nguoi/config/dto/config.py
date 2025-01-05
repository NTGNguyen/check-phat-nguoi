from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from check_phat_nguoi.enums import LogLevelEnum

from .api import ApiEnum
from .notify.telegram_notify import TelegramNotifyDTO
from .plate_info import PlateInfoDTO


class ConfigDTO(BaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)

    plates: tuple[PlateInfoDTO, ...] = Field(
        description="Danh sách các biển xe", default_factory=tuple
    )
    notifications: tuple[TelegramNotifyDTO, ...] = Field(
        description="Danh sách các thiết lập để thông báo", default_factory=tuple
    )
    api: ApiEnum = Field(
        description="Sử dụng API từ trang web nào (mặc định sử dụng API từ trang checkphatnguoi.vn)",
        title="API",
        default=ApiEnum.checkphatnguoi_vn,
    )
    unpaid_only: bool = Field(
        description="Chỉ hiển thị thông tin vi phạm chưa nộp phạt", default=True
    )
    verbose: bool = Field(
        description="Hiển thị tất cả thông tin có thể hiển thị", default=False
    )
    detail_log: bool = True
    log_level: LogLevelEnum = LogLevelEnum.info

    @model_validator(mode="after")
    def validate_type(self) -> Self:
        for plate in self.plates:
            if plate.api is None:
                if self.api not in (ApiEnum.checkphatnguoi_vn,):
                    raise ValueError(
                        f'Plate {plate}: API other than "checkphatnguoi_vn" must set "type"'
                    )
                plate.api = self.api
        return self


__all__ = ["ConfigDTO"]
