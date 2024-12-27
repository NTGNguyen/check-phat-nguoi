from abc import abstractmethod

from check_phat_nguoi.config import PlateInfoDTO
from check_phat_nguoi.config.dto.config import ConfigDTO
from check_phat_nguoi.context import PlateInfoModel


class GetDataBase:
    def __init__(self, plate_infos: tuple[PlateInfoDTO], config: ConfigDTO) -> None:
        self._plate_infos: tuple[PlateInfoDTO] = plate_infos
        self._config = config

    @abstractmethod
    def get_data(self) -> list[PlateInfoModel]:
        pass
