import asyncio
from asyncio import TimeoutError
from logging import getLogger
from typing import override

from aiohttp import (
    ClientError,
    ClientTimeout,
)

from check_phat_nguoi.constants import SEND_MESSAGE_API_URL_TELEGRAM as API_URL
from check_phat_nguoi.context.config import TelegramDTO

from ..markdown_msg import MessagesModel
from .base import NotifyEngineBase

logger = getLogger(__name__)


# FIXME: The message_dict is so ... bruh
class NotifyEngineTelegram(NotifyEngineBase):
    def __init__(self, telegram: TelegramDTO, messages: tuple[MessagesModel, ...]):
        self._telegram: TelegramDTO = telegram
        self._messages: tuple[MessagesModel, ...] = messages
        super().__init__()

    async def _send_message(self, message: str, plate: str) -> None:
        url: str = API_URL.format(bot_token=self._telegram.bot_token)
        payload: dict[str, str] = {
            "chat_id": self._telegram.chat_id,
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
                f"Plate {plate}: Successfully sent to Telegram Chat ID: {self._telegram.chat_id}"
            )
        except TimeoutError as e:
            logger.error(
                f"Plate {plate}: Timeout ({self.timeout}s) sending to Telegram Chat ID: {self._telegram.chat_id}\n{e}"
            )
        except ClientError as e:
            logger.error(
                f"Plate {plate}: Fail to sent to Telegram Chat ID: {self._telegram.chat_id}\n{e}"
            )
        except Exception as e:
            logger.error(e)

    @override
    async def send(self) -> None:
        tasks = (
            self._send_message(message, messages.plate)
            for messages in self._messages
            for message in messages.messages
        )
        await asyncio.gather(*tasks)
