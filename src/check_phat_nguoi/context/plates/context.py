from typing import Final

from check_phat_nguoi.utils.singleton import Singleton

from .models import PlatesModel
from .models.plate_info import PlateInfoModel


class PlatesContext(Singleton, PlatesModel):
    def set_context(self, plates: tuple[PlateInfoModel, ...]) -> None:
        self.plates = plates


plates_context: Final[PlatesContext] = PlatesContext()


__all__ = ["PlatesContext", "plates_context"]
