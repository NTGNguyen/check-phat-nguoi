from __future__ import annotations

from abc import abstractmethod
from logging import getLogger
from typing import Final, Self

from aiohttp import ClientSession, ClientTimeout
from aiohttp.typedefs import LooseHeaders

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.context import PlateDetail
from check_phat_nguoi.types import ApiEnum

logger = getLogger(__name__)


class BaseGetDataEngine:
    api: ApiEnum
    timeout: Final[int] = config.request_timeout

    def __init__(self, *, session_header: LooseHeaders | None = None) -> None:
        self._session_header = session_header
        self._session: ClientSession | None = None

    def create_session(self) -> None:
        if self._session:
            return
        self._session = ClientSession(
            timeout=ClientTimeout(self.timeout),
            headers=self._session_header,
        )
        logger.debug(f"Created get data engine session: {type(self).__name__}")

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        if not self._session:
            return
        await self._session.close()
        logger.debug(f"Closed get data engine session: {type(self).__name__}")

    @abstractmethod
    async def get_data(self, plate_info: PlateInfo) -> PlateDetail | None: ...
