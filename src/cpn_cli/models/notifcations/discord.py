from pydantic import ConfigDict

from cpn_cli.models.notifcations.base import BaseNotificationConfig
from cpn_core.notifications.models.discord import DiscordNotificationEngineConfig


class DiscordNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Discord config",
        frozen=True,
    )

    discord: DiscordNotificationEngineConfig
