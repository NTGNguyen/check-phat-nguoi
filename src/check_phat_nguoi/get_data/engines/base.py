from __future__ import annotations

from abc import abstractmethod
from logging import getLogger
from typing import Self

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.context import PlateDetail

logger = getLogger(__name__)


class BaseGetDataEngine:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None: ...

    @abstractmethod
    async def get_data(self, plate_info: PlateInfo) -> PlateDetail | None: ...
