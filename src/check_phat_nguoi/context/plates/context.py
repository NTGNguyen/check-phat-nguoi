from typing import Final, override

from pydantic import Field

from .models.plate_detail import PlateDetail


class PlatesContext:
    def __init__(self) -> None:
        self._context: tuple[PlateDetail, ...] = Field(
            description="Danh sách các biển xe", default_factory=tuple
        )

    @property
    def plates(self) -> tuple[PlateDetail, ...]:
        """
        Public get prop but not for set

        Returns:
            tuple[PlateInfoModel, ...]
        """
        return self._context

    def set_plates(self, plates: tuple[PlateDetail, ...]) -> None:
        self._context = plates

    # TODO: @NTGNguyen this is for print(plates: list[PlatesModel]), in order to print out as string to stdout in main
    @override
    def __str__(self) -> str: ...


plates_context: Final[PlatesContext] = PlatesContext()


__all__ = ["PlatesContext", "plates_context"]
