from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import (
    BaseNotificationConfig,
    TelegramNotificationConfig,
)
from check_phat_nguoi.config.models import DiscordNotificationConfig
from check_phat_nguoi.config_reader import config
from check_phat_nguoi.context import plates_context

from .engines.discord import DiscordNotificationEngine
from .engines.telegram import TelegramNotificationEngine
from .markdown_message import MarkdownMessage, MarkdownMessageDetail

logger = getLogger(__name__)


class SendNotifications:
    def __init__(self) -> None:
        self._plate_messages: tuple[MarkdownMessageDetail, ...]
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
            MarkdownMessage(plate_detail).generate_message()
            for plate_detail in plates_context.plates
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
