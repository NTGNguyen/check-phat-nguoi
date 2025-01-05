from asyncio import gather
from typing import Self

from check_phat_nguoi.config import ApiEnum, PlateInfoDTO
from check_phat_nguoi.context import PlateInfoModel

from .engine_base import GetDataEngineBase
from .engine_check_phat_nguoi import GetDataEngineCheckPhatNguoi


class GetData:
    def __init__(self, plates: tuple[PlateInfoDTO, ...]) -> None:
        self._plates = plates
        self.cpn: GetDataEngineCheckPhatNguoi = GetDataEngineCheckPhatNguoi()
        self._plates_infos: set[PlateInfoModel] = set()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self.cpn.__aexit__(exc_type, exc_value, exc_tb)

    async def _get_data_for_plate(self, plate: PlateInfoDTO) -> None:
        get_data_engine: GetDataEngineBase
        match plate.api:
            case ApiEnum.checkphatnguoi_vn:
                get_data_engine = self.cpn
            case _:  # Never reach
                raise Exception("No engine for this type")
        plate_info: PlateInfoModel | None = await get_data_engine.get_data(plate)
        if plate_info is None:
            return
        self._plates_infos.add(plate_info)

    async def get_data(self) -> tuple[PlateInfoModel, ...]:
        await gather(*(self._get_data_for_plate(plate) for plate in self._plates))
        return tuple(self._plates_infos)
