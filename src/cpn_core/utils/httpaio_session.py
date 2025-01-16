from logging import getLogger
from typing import Self

from aiohttp import ClientSession, ClientTimeout

logger = getLogger(__name__)

timeout = ClientTimeout(10)
timeout.total


class HttpaioSession:
    def __init__(self, *, timeout: float = 20, **client_session_opts) -> None:
        self._timeout: float = timeout
        self._session: ClientSession = ClientSession(
            timeout=ClientTimeout(timeout), **client_session_opts
        )
        logger.debug(f"Created httpaio session: {type(self).__name__}")

    @property
    def timeout(self) -> float | None:
        return self._timeout

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self._session.close()
        logger.debug(f"Closed httpaio session: {type(self).__name__}")
