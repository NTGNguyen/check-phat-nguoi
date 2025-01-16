from asyncio import gather
from logging import getLogger

from cpn_cli.config_reader import config
from cpn_cli.models import PlateDetail
from cpn_core.message import MarkdownMessage
from cpn_core.models import (
    BaseNotificationConfig,
    DiscordNotificationConfig,
    MessageDetail,
    TelegramNotificationConfig,
)
from cpn_core.notifications.engines.discord import DiscordNotificationEngine
from cpn_core.notifications.engines.telegram import TelegramNotificationEngine

logger = getLogger(__name__)


class Notify:
    def __init__(self, plate_details: tuple[PlateDetail, ...]) -> None:
        self.plate_details: tuple[PlateDetail, ...] = plate_details
        self._plate_messages: tuple[MessageDetail, ...]
        self._telegram_engine: TelegramNotificationEngine
        self._discord_engine: DiscordNotificationEngine

    async def _send_messages(self, notification_config: BaseNotificationConfig) -> None:
        if isinstance(notification_config, TelegramNotificationConfig):
            await self._telegram_engine.send(
                notification_config.telegram, self._plate_messages
            )
        if isinstance(notification_config, DiscordNotificationConfig):
            await self._discord_engine.send(
                notification_config.discord, self._plate_messages
            )

    async def send(self) -> None:
        if not config.notifications:
            logger.debug("No notification was given. Skip notifying")
            return
        self._plate_messages = tuple(
            MarkdownMessage(
                plate_info=plate_detail.plate_info, violations=plate_detail.violations
            ).generate_message()
            for plate_detail in self.plate_details
            if plate_detail.violations
        )
        async with (
            TelegramNotificationEngine() as self._telegram_engine,
            DiscordNotificationEngine() as self._discord_engine,
        ):
            if config.asynchronous:
                await gather(
                    *(
                        self._send_messages(notification)
                        for notification in config.notifications
                        if notification.enabled
                    )
                )
            else:
                for notification in config.notifications:
                    if notification.enabled:
                        await self._send_messages(notification)
