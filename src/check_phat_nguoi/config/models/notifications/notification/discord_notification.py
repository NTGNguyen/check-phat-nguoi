from pydantic import ConfigDict, Field

from ..engine import DiscordNotificationEngineConfig
from .base_notification import BaseNotificationConfig


class DiscordNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Discord và kích hoạt",
        frozen=True,
    )

    discord: DiscordNotificationEngineConfig = Field(
        description="Discord",
    )


__all__ = ["DiscordNotificationConfig"]
