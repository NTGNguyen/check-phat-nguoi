from pydantic import ConfigDict, Field

from .base_notification import BaseNotificationConfig
from .telegram_engine import TelegramNotificationEngineConfig


class TelegramNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Telegram config",
        frozen=True,
    )

    telegram: TelegramNotificationEngineConfig = Field(
        description="Telegram",
    )


__all__ = ["TelegramNotificationConfig"]
