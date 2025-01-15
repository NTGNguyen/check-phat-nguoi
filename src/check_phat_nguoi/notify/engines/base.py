from __future__ import annotations

from abc import abstractmethod
from logging import getLogger
from typing import Self, TypeVar

from check_phat_nguoi.config import BaseNotificationEngineConfig

from ..markdown_message import MarkdownMessageDetail

logger = getLogger(__name__)


T: TypeVar = TypeVar("T", bound=BaseNotificationEngineConfig)


class BaseNotificationEngine[T]:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None: ...

    @abstractmethod
    async def send(
        self,
        engine_config: T,
        plates_messages: tuple[MarkdownMessageDetail, ...],
    ) -> None: ...
