import asyncio
from logging import getLogger
from typing import override

from aiohttp import ClientError

from check_phat_nguoi.config import TelegramNotificationEngineConfig
from check_phat_nguoi.constants import SEND_MESSAGE_API_URL_TELEGRAM as API_URL
from check_phat_nguoi.utils import HttpaioSession

from ..models import MessageDetail
from .base import BaseNotificationEngine

logger = getLogger(__name__)


class TelegramNotificationEngine(
    BaseNotificationEngine[TelegramNotificationEngineConfig], HttpaioSession
):
    def __init__(self) -> None:
        HttpaioSession.__init__(self)

    async def _send_message(
        self, telegram: TelegramNotificationEngineConfig, message: str, plate: str
    ) -> None:
        logger.info(f"Plate {plate}: Sending to Telegram Chat ID: {telegram.chat_id}")
        url: str = API_URL.format(bot_token=telegram.bot_token)
        payload: dict[str, str] = {
            "chat_id": telegram.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        try:
            async with self._session.post(
                url,
                json=payload,
            ) as response:
                response.raise_for_status()
            logger.info(
                f"Plate {plate}: Successfully sent to Telegram Chat ID: {telegram.chat_id}"
            )
        except TimeoutError as e:
            logger.error(
                f"Plate {plate}: Timeout ({self.timeout}s) sending to Telegram Chat ID: {telegram.chat_id}. {e}"
            )
        except ClientError as e:
            logger.error(
                f"Plate {plate}: Fail to sent to Telegram Chat ID: {telegram.chat_id}. {e}"
            )
        except Exception as e:
            logger.error(
                f"Plate {plate}: Fail to sent to Telegram Chat ID (internally): {telegram.chat_id}. {e}"
            )

    @override
    async def send(
        self,
        engine_config: TelegramNotificationEngineConfig,
        plates_messages: tuple[MessageDetail, ...],
    ) -> None:
        await asyncio.gather(
            *(
                self._send_message(
                    telegram=engine_config, message=message, plate=messages.plate
                )
                for messages in plates_messages
                for message in messages.messages
            )
        )

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)
