from asyncio import gather

from check_phat_nguoi.config import BaseNotificationDTO, TelegramNotificationDTO
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.context import plates_context

from .engines.telegram import TelegramNotificationEngine
from .markdown_msg import MdMsg, MessagesModel


class SendNotifications:
    def __init__(self) -> None:
        self._message_dict: tuple[MessagesModel, ...] = tuple(
            MdMsg(plate_info).generate_msg() for plate_info in plates_context.plates
        )
        self._tele: TelegramNotificationEngine

    async def _send_msgs(self, notification: BaseNotificationDTO) -> None:
        if isinstance(notification, TelegramNotificationDTO):
            await self._tele.send(notification.telegram, self._message_dict)

    async def send(self) -> None:
        enabled_notifications: filter[BaseNotificationDTO] = filter(
            lambda notify: notify.enabled, config.notifications
        )
        async with TelegramNotificationEngine() as self._tele:
            await gather(
                *(
                    self._send_msgs(notification)
                    for notification in enabled_notifications
                )
            )
