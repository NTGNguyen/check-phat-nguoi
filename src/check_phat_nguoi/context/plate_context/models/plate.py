from typing import override

from pydantic import BaseModel, Field

from .plate_info import PlateInfoModel


class PlatesModel(BaseModel):
    plates: tuple[PlateInfoModel, ...] = Field(
        description="Danh sách các biển xe", default_factory=tuple
    )

    # TODO: @NTGNguyen this is for print(plates: list[PlatesModel]), in order to print out as string to stdout in main
    @override
    def __str__(self) -> str: ...


__all__ = ["PlatesModel"]
