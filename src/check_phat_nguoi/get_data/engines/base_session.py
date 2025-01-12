from __future__ import annotations

from logging import getLogger
from typing import Final, Self

from aiohttp import ClientSession, ClientTimeout
from aiohttp.typedefs import LooseHeaders

from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.types import ApiEnum

logger = getLogger(__name__)


class BaseGetDataSession:
    # NOTE: I don't know how to force child class override this api field
    api: ApiEnum
    timeout: Final[int] = config.request_timeout

    def __init__(self, *, session_header: LooseHeaders | None = None) -> None:
        self._session: ClientSession = ClientSession(
            timeout=ClientTimeout(self.timeout),
            headers=session_header,
        )
        logger.debug(f"Created get data engine session: {type(self).__name__}")

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self._session.close()
        logger.debug(f"Closed get data engine session: {type(self).__name__}")
