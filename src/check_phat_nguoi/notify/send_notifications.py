from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import (
    BaseNotificationConfig,
    BaseNotificationEngineConfig,
    TelegramNotificationConfig,
)
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.context import plates_context

from .engines.base import BaseNotificationEngine
from .engines.telegram import TelegramNotificationEngine
from .markdown_message import MarkdownMessage, MarkdownMessageDetail

logger = getLogger(__name__)


class SendNotifications:
    def __init__(self) -> None:
        self._md_messages: tuple[MarkdownMessageDetail, ...]
        self._telegram_engine: TelegramNotificationEngine

    async def _send_messages(self, notification: BaseNotificationConfig) -> None:
        notification_engine: BaseNotificationEngine | None = None
        notification_config: BaseNotificationEngineConfig | None = None
        if isinstance(notification, TelegramNotificationConfig):
            notification_engine = self._telegram_engine
            notification_config = notification.telegram
        if notification_config and notification_engine:
            await notification_engine.send(notification_config, self._md_messages)
        else:
            logger.error(
                "There's a undefined notification engine or notification config"
            )  # May never reach this case

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
