from pydantic import ConfigDict

from .base_notification import BaseNotificationConfig
from .discord_engine import DiscordNotificationEngineConfig


class DiscordNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Discord config",
        frozen=True,
    )

    discord: DiscordNotificationEngineConfig


__all__ = ["DiscordNotificationConfig"]
