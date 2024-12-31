import asyncio
from logging import Logger, getLogger

from check_phat_nguoi.config import config
from check_phat_nguoi.config.config_reader import _config_reader
from check_phat_nguoi.context.plate_context.models.plate import PlatesModel
from check_phat_nguoi.get_data.check_phat_nguoi import GetDataCheckPhatNguoi
from check_phat_nguoi.notify.message import Message
from check_phat_nguoi.notify.telegram import Telegram

from .utils.setup_logger import setup_logger

logger: Logger = getLogger(__name__)


async def _main():
    setup_logger()
    logger.debug(config)
    get_data_object = GetDataCheckPhatNguoi(_config_reader().data)
    data = await get_data_object.get_data()
    plate_object = PlatesModel(plates=data)
    message_object = Message(plate_context_object=plate_object)
    message_dict = message_object.format_messages()
    for notify_object in _config_reader().notify:
        telegram_object = Telegram(notify_object, message_dict)
        await telegram_object.send_messages()


def main():
    asyncio.run(_main())


__all__ = ["main"]
