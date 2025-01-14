from __future__ import annotations

from abc import abstractmethod
from logging import getLogger
from typing import Self

from check_phat_nguoi.config import BaseNotificationEngineConfig

from ..markdown_message import MarkdownMessageDetail

logger = getLogger(__name__)


class BaseNotificationEngine:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None: ...

    # FIXME: This is for inheritances. But it have to check inside this method one more time... Which is slow
    @abstractmethod
    async def send(
        self,
        notification_config: BaseNotificationEngineConfig,
        plates_messages: tuple[MarkdownMessageDetail, ...],
    ) -> None: ...
