from __future__ import annotations

import asyncio

from discord import Intents
from discord.ext.commands import Bot

from check_phat_nguoi.config import DiscordNotificationEngineConfig

from ..markdown_message import MarkdownMessageDetail


class DiscordNotificationEngine(Bot):
    def __init__(
        self,
        discord_e: DiscordNotificationEngineConfig,
        messages: MarkdownMessageDetail,
    ):
        super().__init__(command_prefix="!", intents=Intents.default())
        self.discord_e = discord_e
        self.messages = messages

    async def send(
        self,
    ):
        await self._send_messages(self.discord_e.user_id, self.messages)

    async def _send_messages(self, user_id, messages):
        try:
            user = await self.fetch_user(user_id)
            tasks = [self._send_message(user, message) for message in self.messages]
            await asyncio.gather(*tasks)
        except Exception as e:
            # TODO: @NTGNguyen handle later
            print(e)

    async def _send_message(self, user, message):
        await user.send(message)

    async def __aenter__(self):
        await self.start(self.discord_e.bot_token)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
