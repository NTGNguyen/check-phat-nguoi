from pydantic import Field

from .base_notify import BaseNotifyDTO
from .telegram import TelegramDTO


class TelegramNotifyDTO(BaseNotifyDTO):
    telegram: TelegramDTO = Field(
        description="Gửi thông báo đến telegram",
        frozen=True,
    )


__all__ = ["TelegramNotifyDTO"]
