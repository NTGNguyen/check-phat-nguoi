from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import BaseNotificationConfig, TelegramNotificationConfig
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.config.models import DiscordNotificationConfig
from check_phat_nguoi.context import plates_context

from .engines import DiscordNotificationEngine, TelegramNotificationEngine
from .markdown_message import MarkdownMessage, MarkdownMessageDetail

logger = getLogger(__name__)


class SendNotifications:
    def __init__(self) -> None:
        self._md_messages: tuple[MarkdownMessageDetail, ...]
        self._telegram_engine: TelegramNotificationEngine
        self._discord_engine: DiscordNotificationEngine

    async def _send_messages(self, notification: BaseNotificationConfig) -> None:
        if isinstance(notification, TelegramNotificationConfig):
            await self._telegram_engine.send(notification.telegram, self._md_messages)
        if isinstance(notification, DiscordNotificationConfig):
            await DiscordNotificationEngine(
                notification.discord, self._md_messages
            ).send()

    async def send(self) -> None:
        if config.notifications is None:
            logger.debug("No notification was given. Skip notifying")
            return
        self._md_messages = tuple(
            MarkdownMessage(plate_detail).generate_message()
            for plate_detail in plates_context.plates
        )
        async with TelegramNotificationEngine() as self._telegram_engine:
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
