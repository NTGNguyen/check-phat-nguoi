from pydantic import ConfigDict

from cpn_cli.models.notifcations.base import BaseNotificationConfig
from cpn_core.notifications.models.telegram import (
    TelegramNotificationEngineConfig,
)


class TelegramNotificationConfig(BaseNotificationConfig):
    model_config = ConfigDict(
        title="Telegram config",
        frozen=True,
    )

    telegram: TelegramNotificationEngineConfig
