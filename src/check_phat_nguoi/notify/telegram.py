import asyncio
from logging import getLogger
from typing import LiteralString

from aiohttp import ClientConnectionError, ClientSession, ClientTimeout

from check_phat_nguoi.config import TelegramNotifyDTO

from ..modules.constants.notify import SEND_MESSAGE_API_URL_TELEGRAM as API_URL

logger = getLogger(__name__)


class Telegram:
    def __init__(
        self,
        telegram_notify: TelegramNotifyDTO,
        message_dict: dict[str, LiteralString],
    ):
        self._telegram_notify_object: TelegramNotifyDTO = telegram_notify
        self._message_dict: dict[str, LiteralString] = message_dict
        self.timeout = 10

    async def _send_message(self, message: LiteralString) -> None:
        if not self._telegram_notify_object.enabled:
            logger.info("Not enable to sending")
            return
        url = API_URL.format(bot_token=self._telegram_notify_object.telegram.bot_token)
        payload = {
            "chat_id": self._telegram_notify_object.telegram.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        session = ClientSession()
        try:
            async with session.post(
                url, json=payload, timeout=ClientTimeout(self.timeout)
            ) as response:
                response.raise_for_status()
            logger.info(
                "Sending message completed for chat_id:{chat_id} and bot_token:{bot_token}".format(
                    chat_id=self._telegram_notify_object.telegram.chat_id,
                    bot_token=self._telegram_notify_object.telegram.bot_token,
                )
            )
        except asyncio.TimeoutError:
            logger.error(
                "Time out of {self.timeout} seconds for chat_id:{chat_id} and bot_token:{bot_token}".format(
                    chat_id=self._telegram_notify_object.telegram.chat_id,
                    bot_token=self._telegram_notify_object.telegram.bot_token,
                )
            )
        except ClientConnectionError:
            logger.error(
                "Unable to sending message for chat_id:{chat_id} and bot_token:{bot_token}".format(
                    chat_id=self._telegram_notify_object.telegram.chat_id,
                    bot_token=self._telegram_notify_object.telegram.bot_token,
                )
            )
        finally:
            await session.close()

    async def send_messages(self) -> None:
        async def _concurent_send_messages():
            tasks = [
                self._send_message(message) for _, message in self._message_dict.items()
            ]
            await asyncio.gather(*tasks)

        await _concurent_send_messages()
