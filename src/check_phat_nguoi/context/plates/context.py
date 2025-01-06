from typing import Final

from .models import PlatesModel
from .models.plate_info import PlateInfoModel


class PlatesContext:
    def __init__(self) -> None:
        self._context: PlatesModel = PlatesModel()

    @property
    def plates(self) -> tuple[PlateInfoModel, ...]:
        """
        Public get prop but not for set

        Returns:
            tuple[PlateInfoModel, ...]
        """
        return self._context.plates

    def set_plates(self, plates: tuple[PlateInfoModel, ...]) -> None:
        self._context.plates = plates


plates_context: Final[PlatesContext] = PlatesContext()


__all__ = ["PlatesContext", "plates_context"]
