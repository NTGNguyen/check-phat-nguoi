from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import BaseNotificationDTO, TelegramNotificationDTO
from check_phat_nguoi.config_reader import config
from check_phat_nguoi.context import plates_context

from .engines.telegram import TelegramNotificationEngine
from .markdown_message import MarkdownMessage, MessagesModel

logger = getLogger(__name__)


class SendNotifications:
    def __init__(self) -> None:
        self._md_messages: tuple[MessagesModel, ...]
        self._tele: TelegramNotificationEngine

    async def _send_messages(self, notification: BaseNotificationDTO) -> None:
        if isinstance(notification, TelegramNotificationDTO):
            await self._tele.send(notification.telegram, self._md_messages)

    async def send(self) -> None:
        enabled_notifications: tuple[BaseNotificationDTO, ...] = tuple(
            notification
            for notification in config.notifications
            if notification.enabled
        )
        if not enabled_notifications:
            logger.debug("Skip notification")
            return
        logger.debug(f"Enabled notification: {enabled_notifications}")

        self._md_messages = tuple(
            MarkdownMessage(plate_info).generate_message()
            for plate_info in plates_context.plates
        )
        async with TelegramNotificationEngine() as self._tele:
            await gather(
                *(
                    self._send_messages(notification)
                    for notification in enabled_notifications
                )
            )
