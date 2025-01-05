import asyncio
from logging import Logger, getLogger

from check_phat_nguoi.config import config
from check_phat_nguoi.config.dto.notify.base_notify import BaseNotifyDTO
from check_phat_nguoi.config.dto.notify.telegram_notify import TelegramNotifyDTO
from check_phat_nguoi.context import PlatesModel
from check_phat_nguoi.get_data import GetData
from check_phat_nguoi.notify.message import Message
from check_phat_nguoi.notify.noti_engine import NotificationEngine
from check_phat_nguoi.notify.telegram import Telegram

from .utils.setup_logger import setup_logger

logger: Logger = getLogger(__name__)


async def async_main() -> None:
    setup_logger()
    async with GetData(plates=config.plates) as get_data:
        plates: PlatesModel = PlatesModel(plates=await get_data.get_data())
    message_dict = Message(plates=plates).format_messages()
    notifications: filter[BaseNotifyDTO] = filter(
        lambda notify: notify.enabled, config.notifications
    )
    for notification in notifications:
        noti_engine: NotificationEngine
        if isinstance(notification, TelegramNotifyDTO):
            noti_engine = Telegram(notification.telegram, message_dict)
        else:
            continue  # Unknown notification engine
        await noti_engine.send_messages()


def main() -> None:
    asyncio.run(async_main())


__all__ = ["main"]
