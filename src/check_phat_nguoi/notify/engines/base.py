from __future__ import annotations

from logging import getLogger
from typing import Self

logger = getLogger(__name__)


class BaseNotificationEngine:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None: ...
