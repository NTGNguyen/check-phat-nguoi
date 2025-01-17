import asyncio
from logging import getLogger
from typing import LiteralString, override

from aiohttp import ClientError, ClientSession, ClientTimeout

from cpn_core.notifications.models.telegram import (
    TelegramNotificationEngineConfig,
)

from .base import BaseNotificationEngine

API_URL: LiteralString = "https://api.telegram.org/bot{bot_token}/sendMessage"


logger = getLogger(__name__)


class TelegramNotificationEngine(
    BaseNotificationEngine[TelegramNotificationEngineConfig]
):
    def __init__(self, *, timeout: float) -> None:
        self._timeout: float = timeout
        self._session: ClientSession = ClientSession(
            timeout=ClientTimeout(timeout),
        )

    async def _send_message(
        self,
        telegram: TelegramNotificationEngineConfig,
        message: str,
    ) -> None:
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
            logger.info(f"Successfully sent to Telegram Chat ID: {telegram.chat_id}")
        except TimeoutError as e:
            logger.error(
                f"Timeout ({self._timeout}s) sending to Telegram Chat ID: {telegram.chat_id}. {e}"
            )
            raise
        except ClientError as e:
            logger.error(f"Failed to sent to Telegram Chat ID: {telegram.chat_id}. {e}")
            raise
        except Exception as e:
            logger.error(
                f"Failed to sent to Telegram Chat ID (internally): {telegram.chat_id}. {e}"
            )
            raise

    @override
    async def send(
        self,
        config: TelegramNotificationEngineConfig,
        messages: tuple[str, ...],
    ) -> None:
        await asyncio.gather(
            *(
                self._send_message(
                    telegram=config,
                    message=message,
                )
                for message in messages
            )
        )

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self._session.close()
