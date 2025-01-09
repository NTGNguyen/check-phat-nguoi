from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.context import (
    PlateDetail,
    plates_context,
)
from check_phat_nguoi.types import ApiEnum

from .engines import BaseGetDataEngine, GetDataEngineCheckPhatNguoi

logger = getLogger(__name__)


class GetData:
    def __init__(self) -> None:
        self._engine_cpn: GetDataEngineCheckPhatNguoi
        self._plates_infos: set[PlateDetail] = set()

    async def _get_data_for_plate(self, plate_info: PlateInfo) -> None:
        plate_detail: PlateDetail | None
        if plate_info.api == ApiEnum.all or (
            plate_info.api is None and config.api == ApiEnum.all
        ):
            plate_detail = await self._engine_cpn.get_data(plate_info)
            # TODO: This is for later other API engine is done
            # if plate_info is None:
            #     plate_info = await self.csgt.get_data(plate)
        else:
            get_data_engine: BaseGetDataEngine
            match api := (plate_info.api or config.api):
                case ApiEnum.checkphatnguoi_vn:
                    get_data_engine = self._engine_cpn
                case ApiEnum.csgt_vn:
                    # TODO: @Nguyen thay get_data_engine
                    logger.error("csgt.vn has't been implemented yet")
                    return
                case _:  # Never reach
                    logger.error(f"Plate {plate_info.plate} - {api}: Not defined!")
                    return
            logger.info(f"Plate {plate_info.plate}: Getting data...")
            plate_detail = await get_data_engine.get_data(plate_info)
        if plate_detail is None:
            return
        self._plates_infos.add(plate_detail)

    async def get_data(self) -> None:
        async with GetDataEngineCheckPhatNguoi() as self._engine_cpn:
            await gather(
                *(self._get_data_for_plate(plate_info) for plate_info in config.plates)
            )
            plates_context.set_plates(plates=tuple(self._plates_infos))
