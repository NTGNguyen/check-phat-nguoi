from logging import getLogger
from typing import override

from discord import (
    Client,
    DMChannel,
    Forbidden,
    GroupChannel,
    HTTPException,
    Intents,
    TextChannel,
    User,
)

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
        self._client = Client(intents=Intents.default())

    async def _send_channel(self) -> None:
        try:
            channel = await self._client.fetch_channel(self.discord.chat_id)
            if channel is None:
                logger.error(f"Discord channel ID {self.discord.chat_id}: Not found")
                return
            if (
                not isinstance(channel, TextChannel)
                or not isinstance(channel, GroupChannel)
                or not isinstance(channel, DMChannel)
            ):
                logger.error(
                    f"Discord channel ID {self.discord.chat_id}: Must be text channel"
                )
                return
            for message in self._messages:
                await channel.send(message)
            logger.info(f"Successfully sent to Discord channel: {self.discord.chat_id}")
        except Exception as e:
            logger.error(f"Discord channel ID {self.discord.chat_id}: {e}")

    async def _send_user(self) -> None:
        try:
            user: User = await self._client.fetch_user(self.discord.chat_id)
            for message in self._messages:
                await user.send(message)
            logger.info(f"Successfully sent to Discord user: {self.discord.chat_id}")
        except Forbidden as e:
            logger.error(
                f"Discord bot doesn't have permission to send to user {self.discord.chat_id}. {e}"
            )
        except HTTPException as e:
            logger.error(f"Failed to send message to {self.discord.chat_id}. {e}")
        except Exception as e:
            logger.error(
                f"Failed to send message to {self.discord.chat_id} (internal). {e}"
            )

    async def send(self) -> None:
        @self._client.event
        async def on_ready() -> None:
            match self.discord.chat_type:
                case "user":
                    await self._send_user()
                case "channel":
                    await self._send_channel()
            await self._client.close()

        await self._client.start(self.discord.bot_token)


class DiscordNotificationEngine(
    BaseNotificationEngine[DiscordNotificationEngineConfig]
):
    @override
    async def send(
        self,
        config: DiscordNotificationEngineConfig,
        messages: tuple[str, ...],
    ) -> None:
        discord_engine = _DiscordNotificationCoreEngine(config, messages)
        await discord_engine.send()
