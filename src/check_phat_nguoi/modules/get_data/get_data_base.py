from abc import abstractmethod

from check_phat_nguoi.config import PlateInfoDTO
from check_phat_nguoi.context import PlateInfoModel


class GetDataBase:
    def __init__(self, plate_infos: list[PlateInfoDTO]) -> None:
        self._plate_infos: list[PlateInfoDTO] = plate_infos

    @abstractmethod
    def get_data(self) -> list[PlateInfoModel]:
        pass
