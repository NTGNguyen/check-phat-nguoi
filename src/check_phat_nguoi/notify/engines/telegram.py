from __future__ import annotations

import asyncio
from asyncio import TimeoutError
from logging import getLogger

from aiohttp import ClientError

from check_phat_nguoi.config import TelegramNotificationEngineConfig
from check_phat_nguoi.constants import SEND_MESSAGE_API_URL_TELEGRAM as API_URL

from ..markdown_message import MarkdownMessageDetail
from .base import BaseNotificationEngine

logger = getLogger(__name__)


class TelegramNotificationEngine(BaseNotificationEngine):
    def __init__(self):
        super().__init__()

    async def send(
        self,
        telegram: TelegramNotificationEngineConfig,
        messages: tuple[MarkdownMessageDetail, ...],
    ) -> None:
        async def _send_message(message: str, plate: str) -> None:
            logger.info(
                f"Plate {plate}: Sending to Telegram Chat ID: {telegram.chat_id}"
            )
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

        await asyncio.gather(
            *(
                _send_message(violation, message.plate)
                for message in messages
                for violation in message.violations
            )
        )
