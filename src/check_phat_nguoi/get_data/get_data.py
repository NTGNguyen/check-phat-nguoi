from asyncio import gather
from logging import getLogger

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.config_reader import config
from check_phat_nguoi.context import (
    PlateDetail,
    plates_context,
)
from check_phat_nguoi.get_data.engines.phat_nguoi import PhatNguoiGetDataEngine
from check_phat_nguoi.types import ApiEnum

from .engines import BaseGetDataEngine, CheckPhatNguoiGetDataEngine, CsgtGetDataEngine

logger = getLogger(__name__)


class GetData:
    def __init__(self) -> None:
        self._checkphatnguoi_engine: CheckPhatNguoiGetDataEngine
        self._csgt_engine: CsgtGetDataEngine
        self._phatnguoi_engine: PhatNguoiGetDataEngine
        self._plates_details: set[PlateDetail] = set()

    async def _get_data_for_plate(self, plate_info: PlateInfo) -> None:
        # NOTE: The config has constraint that config.api will be at least 1 api in tuple
        apis: tuple[ApiEnum, ...] = (
            plate_info.api
            if isinstance(plate_info.api, tuple)
            else (plate_info.api,)
            if plate_info.api
            else config.api
            if isinstance(config.api, tuple)
            else (config.api,)
        )
        engine: BaseGetDataEngine
        for api in apis:
            match api:
                case ApiEnum.checkphatnguoi_vn:
                    engine = self._checkphatnguoi_engine
                case ApiEnum.csgt_vn:
                    engine = self._csgt_engine
                case ApiEnum.phatnguoi_vn:
                    engine = self._phatnguoi_engine
            logger.info(
                f"Plate {plate_info.plate}: Getting data with API: {api.value}..."
            )

            plate_detail: PlateDetail | None = await engine.get_data(plate_info)
            if plate_detail:
                self._plates_details.add(plate_detail)
                break

    async def get_data(self) -> None:
        async with (
            CheckPhatNguoiGetDataEngine() as self._checkphatnguoi_engine,
            CsgtGetDataEngine() as self._csgt_engine,
            PhatNguoiGetDataEngine() as self._phatnguoi_engine,
        ):
            if config.asynchronous:
                await gather(
                    *(
                        self._get_data_for_plate(plate_info)
                        for plate_info in config.plates_infos
                        if plate_info.enabled
                    )
                )
            else:
                for plate_info in config.plates_infos:
                    if plate_info.enabled:
                        await self._get_data_for_plate(plate_info)
            plates_context.set_plates(plates=tuple(self._plates_details))
