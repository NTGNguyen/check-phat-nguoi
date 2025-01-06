from check_phat_nguoi.context import BaseNotifyDTO, TelegramNotifyDTO, plates_context
from check_phat_nguoi.context.config.config_reader import config

from .engines.base import NotifyEngineBase
from .engines.telegram import NotifyEngineTelegram
from .markdown_msg import MdMsg, MessagesModel


class SendNotifications:
    def __init__(self) -> None:
        self._message_dict: tuple[MessagesModel, ...] = tuple(
            MdMsg(plate_info).generate_msg() for plate_info in plates_context.plates
        )

    async def send(self) -> None:
        # FIXME: use with async to auto create / close session
        notifications: filter[BaseNotifyDTO] = filter(
            lambda notify: notify.enabled, config.notifications
        )
        for notification in notifications:
            noti_engine: NotifyEngineBase
            if isinstance(notification, TelegramNotifyDTO):
                noti_engine = NotifyEngineTelegram(
                    notification.telegram, self._message_dict
                )
            else:
                continue  # Unknown notification engine
            await noti_engine.send()
