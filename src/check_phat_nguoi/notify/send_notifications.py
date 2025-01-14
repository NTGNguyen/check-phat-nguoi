from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import (
    BaseNotificationConfig,
    BaseNotificationEngineConfig,
    TelegramNotificationConfig,
)
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.config.models import DiscordNotificationConfig
from check_phat_nguoi.context import plates_context

from .engines.base import BaseNotificationEngine
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
        engine: BaseNotificationEngine | None = None
        engine_config: BaseNotificationEngineConfig | None = None
        if isinstance(notification_config, TelegramNotificationConfig):
            engine = self._telegram_engine
            engine_config = notification_config.telegram
        if isinstance(notification_config, DiscordNotificationConfig):
            engine = self._telegram_engine
            engine_config = notification_config.discord
        if engine and engine_config:
            await engine.send(engine_config, self._plate_messages)
        else:
            logger.error(
                "There's a undefined notification engine or notification config"
            )  # May never reach this case

    async def send(self) -> None:
        if config.notifications is None:
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
