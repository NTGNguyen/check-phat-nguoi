import asyncio
from logging import getLogger

from aiohttp import ClientConnectionError, ClientSession, ClientTimeout

from check_phat_nguoi.config.dto.notify.telegram import TelegramDTO

from ..constants.notify import SEND_MESSAGE_API_URL_TELEGRAM as API_URL
from .noti_engine import NotificationEngine

logger = getLogger(__name__)


class Telegram(NotificationEngine):
    # FIXME: The message_dict is so ... bruh
    def __init__(
        self,
        telegram: TelegramDTO,
        message_dict: dict[str, tuple[str, ...]],
    ):
        self._telegram: TelegramDTO = telegram
        self._message_dict: dict[str, tuple[str, ...]] = message_dict
        # FIXME: Heyyyyy refactor timeout hehe
        self.timeout = 10
        self.session: ClientSession = ClientSession()

    async def _send_message(self, message: str) -> None:
        # FIXME: specify which plate is successfully send, or fail
        # FIXME: use fstring instead of string format
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
                "Sending message completed for chat_id:{chat_id} and bot_token:{bot_token}".format(
                    chat_id=self._telegram.chat_id,
                    bot_token=self._telegram.bot_token,
                )
            )
        except asyncio.TimeoutError:
            logger.error(
                "Time out of {self.timeout} seconds for chat_id:{chat_id} and bot_token:{bot_token}".format(
                    chat_id=self._telegram.chat_id,
                    bot_token=self._telegram.bot_token,
                )
            )
        except ClientConnectionError:
            logger.error(
                f"Unable to sending message for chat_id:{self._telegram.chat_id} and bot_token:{self._telegram.bot_token}"
            )
        except Exception as e:
            logger.error(e)

    async def send_messages(self) -> None:
        tasks = (
            self._send_message(message)
            for message_tuple in self._message_dict.values()
            for message in message_tuple
        )
        await asyncio.gather(*tasks)
        await self.session.close()
