from abc import abstractmethod

from check_phat_nguoi.models.context.plate_context.plate_info import (
    PlateInfoContextModel,
)
from check_phat_nguoi.models.plate_info import PlateInfoModel


class GetDataBase:
    def __init__(self, plate_infos: list[PlateInfoModel]) -> None:
        self._plate_infos: list[PlateInfoModel] = plate_infos

    @abstractmethod
    def get_data(self) -> list[PlateInfoContextModel]:
        pass
