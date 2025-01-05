from asyncio import gather

from check_phat_nguoi.config import ApiEnum, PlateInfoDTO, config
from check_phat_nguoi.context import PlateInfoModel, plates_context

from .engine_base import GetDataEngineBase
from .engine_check_phat_nguoi import GetDataEngineCheckPhatNguoi


class GetData:
    def __init__(self) -> None:
        self.cpn: GetDataEngineCheckPhatNguoi
        self._plates_infos: set[PlateInfoModel] = set()

    async def _get_data_for_plate(self, plate: PlateInfoDTO) -> None:
        plate_info: PlateInfoModel | None
        if plate.api == ApiEnum.all or (
            plate.api is None and config.api == ApiEnum.all
        ):
            plate_info = await self.cpn.get_data(plate)
            # TODO: This is for later other API engine is done
            # if plate_info is None:
            #     plate_info = await self.csgt.get_data(plate)
        else:
            get_data_engine: GetDataEngineBase
            match plate.api or config.api:
                case ApiEnum.checkphatnguoi_vn:
                    get_data_engine = self.cpn
                case ApiEnum.csgt_vn:
                    # TODO: @Nguyen thay get_data_engine
                    raise NotImplementedError("csgt.vn has't been implemented yet")
                case _:  # Never reach
                    raise Exception("No engine for this type")
            plate_info = await get_data_engine.get_data(plate)
        if plate_info is None:
            return
        self._plates_infos.add(plate_info)

    async def get_data(self) -> None:
        async with GetDataEngineCheckPhatNguoi() as self.cpn:
            await gather(*(self._get_data_for_plate(plate) for plate in config.plates))
            plates_context.set_context(plates=tuple(self._plates_infos))
