from pydantic import ConfigDict, Field

from .base_notification import BaseNotificationConfig
from .discord_engine import DiscordNotificationEngineConfig


class DiscordNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Discord config",
        frozen=True,
    )

    discord: DiscordNotificationEngineConfig = Field(
        description="Discord",
    )


__all__ = ["DiscordNotificationConfig"]
