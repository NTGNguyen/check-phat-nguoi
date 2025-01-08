from __future__ import annotations

from logging import getLogger
from typing import Final, Self

from aiohttp import ClientSession, ClientTimeout
from aiohttp.typedefs import LooseHeaders

from check_phat_nguoi.config.config_reader import config

logger = getLogger(__name__)


class BaseNotificationEngine:
    timeout: Final[int] = config.request_timeout

    def __init__(self, *, session_header: LooseHeaders | None = None) -> None:
        self.session: ClientSession = ClientSession(
            timeout=ClientTimeout(self.timeout),
            headers=session_header,
        )
        logger.debug(f"Created notify engine session: {type(self).__name__}")

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        logger.debug(f"Closed notify engine session: {type(self).__name__}")
        await self.session.close()
