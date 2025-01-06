from typing import Final, Self

from aiohttp import ClientSession

from check_phat_nguoi.config.config_reader import config


class BaseNotificationEngine:
    timeout: Final[int] = config.request_timeout

    def __init__(self) -> None:
        self.session: ClientSession = ClientSession()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self.session.close()
