import asyncio
from asyncio import TimeoutError
from logging import getLogger

from aiohttp import (
    ClientError,
    ClientTimeout,
)

from check_phat_nguoi.config import TelegramNotificationEngineDTO
from check_phat_nguoi.constants import SEND_MESSAGE_API_URL_TELEGRAM as API_URL

from ..markdown_message import MessagesModel
from .base import BaseNotificationEngine

logger = getLogger(__name__)


# FIXME: The message_dict is so ... bruh
class TelegramNotificationEngine(BaseNotificationEngine):
    def __init__(self):
        super().__init__()

    async def send(
        self,
        telegram: TelegramNotificationEngineDTO,
        messages: tuple[MessagesModel, ...],
    ) -> None:
        async def _send_message(message: str, plate: str) -> None:
            url: str = API_URL.format(bot_token=telegram.bot_token)
            payload: dict[str, str] = {
                "chat_id": telegram.chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            # session: ClientSession = ClientSession()
            try:
                async with self.session.post(
                    url, json=payload, timeout=ClientTimeout(self.timeout)
                ) as response:
                    response.raise_for_status()
                logger.info(
                    f"Plate {plate}: Successfully sent to Telegram Chat ID: {telegram.chat_id}"
                )
            except TimeoutError as e:
                logger.error(
                    f"Plate {plate}: Timeout ({self.timeout}s) sending to Telegram Chat ID: {telegram.chat_id}\n{e}"
                )
            except ClientError as e:
                logger.error(
                    f"Plate {plate}: Fail to sent to Telegram Chat ID: {telegram.chat_id}\n{e}"
                )
            except Exception as e:
                logger.error(e)

        # TODO: the violation name conventno is not match with param message :v
        tasks = (
            _send_message(violation, message.plate)
            for message in messages
            for violation in message.violations
        )
        await asyncio.gather(*tasks)
