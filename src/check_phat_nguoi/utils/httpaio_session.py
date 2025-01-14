from __future__ import annotations

from logging import getLogger
from typing import Any, Final, Self

from aiohttp import ClientSession, ClientTimeout

from check_phat_nguoi.config.config_reader import config

logger = getLogger(__name__)

timeout = ClientTimeout(10)
timeout.total


class HttpaioSession:
    _timeout: Final[ClientTimeout] = ClientTimeout(config.request_timeout)

    def __init__(self, **options: dict[str, Any]) -> None:
        self._options: dict[str, Any] = {"timeout": self._timeout} | options
        self._session: ClientSession = ClientSession(**self._options)
        logger.debug(f"Created httpaio session: {type(self).__name__}")

    @property
    def timeout(self) -> float | None:
        return self._timeout.total

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self._session.close()
        logger.debug(f"Closed httpaio session: {type(self).__name__}")
