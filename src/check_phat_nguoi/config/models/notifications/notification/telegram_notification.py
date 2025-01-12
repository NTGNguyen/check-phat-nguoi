from pydantic import ConfigDict, Field

from ..engine import TelegramNotificationEngineConfig
from .base_notification import BaseNotificationConfig


class TelegramNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Telegram và kích hoạt",
        frozen=True,
    )

    telegram: TelegramNotificationEngineConfig = Field(
        description="Telegram",
    )


__all__ = ["TelegramNotificationConfig"]
