import asyncio
from logging import getLogger
from typing import override

from discord import Intents, NotFound, User
from discord.ext.commands import Bot

from cpn_core.notifications.models.discord import DiscordNotificationEngineConfig

from .base import BaseNotificationEngine

logger = getLogger(__name__)


# FIXME: @NTGNguyen: fetch channel, id bla bla bla. The command_prefix seem bruh? not relate
class _DiscordNotificationCoreEngine:
    def __init__(
        self,
        discord: DiscordNotificationEngineConfig,
        messages: tuple[str, ...],
    ) -> None:
        self.discord: DiscordNotificationEngineConfig = discord
        self._messages: tuple[str, ...] = messages
        self.bot = Bot(command_prefix="!", intents=Intents.default())
        self.user: User

    async def _send_message(self, message: str) -> None:
        try:
            await self.user.send(message)
        except Exception as e:
            logger.error(f"Failed to send message to {self.user}. {e}")
            raise

    async def send(self) -> None:
        try:
            self.user = await self.bot.fetch_user(self.discord.chat_id)
            await asyncio.gather(
                *(self._send_message(message) for message in self._messages)
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


class DiscordNotificationEngine(
    BaseNotificationEngine[DiscordNotificationEngineConfig]
):
    @override
    async def send(
        self,
        config: DiscordNotificationEngineConfig,
        messages: tuple[str, ...],
    ) -> None:
        async with _DiscordNotificationCoreEngine(config, messages) as core_engine:
            await core_engine.send()
