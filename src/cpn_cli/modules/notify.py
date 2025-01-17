from asyncio import gather
from functools import cache, cached_property
from logging import getLogger

from cpn_cli.models.notifcations.base import BaseNotificationConfig
from cpn_cli.models.notifcations.discord import DiscordNotificationConfig
from cpn_cli.models.notifcations.telegram import TelegramNotificationConfig
from cpn_cli.modules.config_reader import config
from cpn_core.models.plate_detail import PlateDetail
from cpn_core.notifications.engines.discord import DiscordNotificationEngine
from cpn_core.notifications.engines.telegram import TelegramNotificationEngine

logger = getLogger(__name__)


class Notify:
    def __init__(self, plate_details: tuple[PlateDetail, ...]) -> None:
        self._plate_details: tuple[PlateDetail, ...] = plate_details
        self._telegram_engine: TelegramNotificationEngine
        self._discord_engine: DiscordNotificationEngine

    @cached_property
    def _raw_messages(self) -> tuple[tuple[str, ...], ...]:
        return tuple(
            plate_detail.get_strs(
                show_less_detail=config.show_less_details, markdown=False
            )
            for plate_detail in self._plate_details
        )

    @cached_property
    def _markdown_messages(self) -> tuple[tuple[str, ...], ...]:
        return tuple(
            plate_detail.get_strs(
                show_less_detail=config.show_less_details, markdown=True
            )
            for plate_detail in self._plate_details
        )

    @cache
    def _get_messages_groups(self, markdown: bool) -> tuple[tuple[str, ...], ...]:
        return tuple(
            plate_detail.get_strs(
                show_less_detail=config.show_less_details, markdown=markdown
            )
            for plate_detail in self._plate_details
        )

    async def _send_messages(self, notification_config: BaseNotificationConfig) -> None:
        try:
            if isinstance(notification_config, TelegramNotificationConfig):
                for messages in self._get_messages_groups(
                    notification_config.telegram.markdown
                ):
                    await self._telegram_engine.send(
                        notification_config.telegram, messages
                    )
            elif isinstance(notification_config, DiscordNotificationConfig):
                for messages in self._get_messages_groups(
                    notification_config.discord.markdown
                ):
                    await self._discord_engine.send(
                        notification_config.discord, messages
                    )
            else:
                logger.error("Unknown notification config!")
                return
        except Exception as e:
            logger.error(f"Failed to sent notification. {e}")

    async def send(self) -> None:
        if not config.notifications:
            logger.debug("No notification was given. Skip notifying")
            return
        async with (
            TelegramNotificationEngine(
                timeout=config.request_timeout
            ) as self._telegram_engine,
            DiscordNotificationEngine() as self._discord_engine,
        ):
            if config.asynchronous:
                await gather(
                    *(
                        self._send_messages(notification)
                        for notification in config.notifications
                        if notification.enabled
                    )
                )
            else:
                for notification in config.notifications:
                    if notification.enabled:
                        await self._send_messages(notification)
