from abc import abstractmethod

from check_phat_nguoi.config import PlateInfoDTO
from check_phat_nguoi.context import PlateInfoModel


class GetDataBase:
    def __init__(self, plate_infos: tuple[PlateInfoDTO, ...]) -> None:
        self._plate_infos: tuple[PlateInfoDTO, ...] = plate_infos

    @abstractmethod
    async def get_data(self) -> tuple[PlateInfoModel, ...]: ...
