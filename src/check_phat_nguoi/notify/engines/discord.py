from __future__ import annotations

import asyncio
from logging import getLogger

from discord import Intents, NotFound, User
from discord.ext.commands import Bot

from check_phat_nguoi.config import DiscordNotificationEngineConfig

from ..markdown_message import MarkdownMessageDetail
from .base import BaseNotificationEngine

logger = getLogger(__name__)


class DiscordNotificationEngine(BaseNotificationEngine):
    def __init__(
        self,
        discord: DiscordNotificationEngineConfig,
        messages: tuple[MarkdownMessageDetail, ...],
    ) -> None:
        self.discord: DiscordNotificationEngineConfig = discord
        self.messages: tuple[MarkdownMessageDetail, ...] = messages
        self.bot = Bot(command_prefix="!", intents=Intents.default())
        self.user: User

    async def _send_message(self, message: str, plate: str) -> None:
        try:
            await self.user.send(message)
        except Exception as e:
            logger.error(f"Plate {plate}: Failed to send message to {self.user}. {e}")

    async def send(self) -> None:
        try:
            self.user = await self.bot.fetch_user(self.discord.user_id)
            await asyncio.gather(
                *(
                    self._send_message(violation, message.plate)
                    for message in self.messages
                    for violation in message.violations
                )
            )
        # TODO: @NTGNguyen handle later
        except NotFound as _:
            ...
        except Exception as e:
            print(e)

    async def __aenter__(self):
        await self.bot.start(self.discord.bot_token)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.bot.close()
