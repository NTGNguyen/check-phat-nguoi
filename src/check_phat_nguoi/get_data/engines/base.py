from __future__ import annotations

from abc import abstractmethod
from logging import getLogger
from typing import Final, Self

from aiohttp import ClientSession

from check_phat_nguoi.config import PlateInfoDTO
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.context import PlateInfoModel

logger = getLogger(__name__)


class BaseGetDataEngine:
    timeout: Final[int] = config.request_timeout

    def __init__(self) -> None:
        self.session: ClientSession = ClientSession()
        logger.debug(f"Established get data engine session: {type(self).__name__}")

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self.session.close()
        logger.debug(f"Closed data engine session: {type(self).__name__}")

    @abstractmethod
    async def get_data(self, plate: PlateInfoDTO) -> PlateInfoModel | None: ...
