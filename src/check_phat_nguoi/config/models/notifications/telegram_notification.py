from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel

from .base_notification import BaseNotificationConfig
from .telegram_engine import TelegramNotificationEngineConfig


class TelegramNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Telegram và kích hoạt",
        alias_generator=to_camel,
    )

    telegram: TelegramNotificationEngineConfig = Field(
        description="Telegram",
        frozen=True,
    )


__all__ = ["TelegramNotificationConfig"]
