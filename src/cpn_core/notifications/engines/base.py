from abc import abstractmethod
from logging import getLogger
from typing import Self, TypeVar

from cpn_core.notifications.models.base import BaseNotificationEngineConfig

logger = getLogger(__name__)


T: TypeVar = TypeVar("T", bound=BaseNotificationEngineConfig)


class BaseNotificationEngine[T]:
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None: ...

    @abstractmethod
    async def send(
        self,
        config: T,
        messages: tuple[str, ...],
    ) -> None: ...
