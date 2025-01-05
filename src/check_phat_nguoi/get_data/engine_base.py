from abc import abstractmethod
from typing import Self

from aiohttp import ClientSession

from check_phat_nguoi.config import PlateInfoDTO
from check_phat_nguoi.context import PlateInfoModel


class GetDataEngineBase:
    def __init__(self) -> None:
        self.session: ClientSession = ClientSession()

    async def __aenter__(self) -> Self:
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self.session.close()

    @abstractmethod
    async def get_data(self, plate: PlateInfoDTO) -> PlateInfoModel | None: ...
