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
        self._plates_details: set[PlateDetail] = set()

    async def _get_data_for_plate(self, plate_info: PlateInfo) -> None:
        # NOTE: The config has constraint that config.api will be at least 1 api in tuple
        apis: tuple[ApiEnum, ...] = (
            plate_info.api
            if isinstance(plate_info.api, tuple)
            else (plate_info.api,)
            if plate_info.api is not None
            else config.api
            if isinstance(config.api, tuple)
            else (config.api,)
        )
        get_data_engine: BaseGetDataEngine
        for api in apis:
            match api:
                case ApiEnum.checkphatnguoi_vn:
                    get_data_engine = self._engine_cpn
                case ApiEnum.csgt_vn:
                    # TODO: @Nguyen thay get_data_engine
                    logger.error("csgt.vn has't been implemented yet")
                    return
            logger.info(
                f"Plate {plate_info.plate}: Getting data with API: {api.value}..."
            )

            plate_detail: PlateDetail | None = await get_data_engine.get_data(
                plate_info
            )
            if plate_detail is not None:
                self._plates_details.add(plate_detail)
                return

    async def get_data(self) -> None:
        async with GetDataEngineCheckPhatNguoi() as self._engine_cpn:
            await gather(
                *(
                    self._get_data_for_plate(plate_info)
                    for plate_info in config.plates_infos
                )
            )
            plates_context.set_plates(plates=tuple(self._plates_details))
