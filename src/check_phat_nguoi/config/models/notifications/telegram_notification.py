from pydantic import ConfigDict

from .base_notification import BaseNotificationConfig
from .telegram_engine import TelegramNotificationEngineConfig


class TelegramNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Telegram config",
        frozen=True,
    )

    telegram: TelegramNotificationEngineConfig


__all__ = ["TelegramNotificationConfig"]
