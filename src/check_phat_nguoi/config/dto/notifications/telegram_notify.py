from pydantic import Field

from .base_notify import BaseNotificationDTO
from .telegram_engine import TelegramNotificationEngineDTO


class TelegramNotificationDTO(BaseNotificationDTO):
    telegram: TelegramNotificationEngineDTO = Field(
        description="Gửi thông báo đến telegram",
        frozen=True,
    )


__all__ = ["TelegramNotificationDTO"]
