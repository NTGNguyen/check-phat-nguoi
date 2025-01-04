import asyncio
from logging import getLogger

from aiohttp import ClientConnectionError, ClientSession, ClientTimeout

from check_phat_nguoi.config.dto.notify.telegram import TelegramDTO

from ..constants.notify import SEND_MESSAGE_API_URL_TELEGRAM as API_URL
from .message import MessagesModel
from .noti_engine import NotificationEngine

logger = getLogger(__name__)


class Telegram(NotificationEngine):
    # FIXME: The message_dict is so ... bruh
    def __init__(
        self, telegram: TelegramDTO, messages: tuple[MessagesModel, ...], timeout=10
    ):
        self._telegram: TelegramDTO = telegram
        self._messages: tuple[MessagesModel, ...] = messages
        # FIXME: Heyyyyy refactor timeout hehe
        self.timeout = timeout
        self.session: ClientSession = ClientSession()

    async def _send_message(self, message: str, plate: str) -> None:
        url = API_URL.format(bot_token=self._telegram.bot_token)
        payload = {
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
        except asyncio.TimeoutError:
            logger.error(
                f"Plate {plate}: Timeout ({self.timeout}s) sending to Telegram Chat ID: {self._telegram.chat_id}"
            )
        except ClientConnectionError:
            logger.error(
                f"Plate {plate}: Fail to sent to Telegram Chat ID: {self._telegram.chat_id}"
            )
        except Exception as e:
            logger.error(e)

    async def send_messages(self) -> None:
        tasks = (
            self._send_message(message, messages.plate)
            for messages in self._messages
            for message in messages.messages
        )
        await asyncio.gather(*tasks)
        await self.session.close()
