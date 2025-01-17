from asyncio import gather
from logging import getLogger

from cpn_cli.models.plate_detail import PlateDetail
from cpn_cli.modules.config_reader import config
from cpn_core.get_data.engines.base import BaseGetDataEngine
from cpn_core.get_data.engines.check_phat_nguoi import CheckPhatNguoiGetDataEngine
from cpn_core.get_data.engines.csgt import CsgtGetDataEngine
from cpn_core.get_data.engines.phat_nguoi import PhatNguoiGetDataEngine
from cpn_core.get_data.engines.zm_io import ZMIOGetDataEngine
from cpn_core.models.plate_info import PlateInfo
from cpn_core.models.violation_detail import ViolationDetail
from cpn_core.types.api import ApiEnum

logger = getLogger(__name__)


class GetData:
    def __init__(self) -> None:
        self._checkphatnguoi_engine: CheckPhatNguoiGetDataEngine
        self._csgt_engine: CsgtGetDataEngine
        self._phatnguoi_engine: PhatNguoiGetDataEngine
        self._zmio_engine: ZMIOGetDataEngine
        self._plate_details: set[PlateDetail] = set()

    async def _get_data_for_plate(self, plate_info: PlateInfo) -> None:
        # NOTE: The config has constraint that config.api will be at least 1 api in tuple
        apis: tuple[ApiEnum, ...] = plate_info.apis if plate_info.apis else config.apis
        engine: BaseGetDataEngine
        for api in apis:
            match api:
                case ApiEnum.checkphatnguoi_vn:
                    engine = self._checkphatnguoi_engine
                case ApiEnum.csgt_vn:
                    engine = self._csgt_engine
                case ApiEnum.phatnguoi_vn:
                    engine = self._phatnguoi_engine
                case ApiEnum.zm_io_vn:
                    engine = self._zmio_engine
            logger.info(
                f"Plate {plate_info.plate}: Getting data with API: {api.value}..."
            )
            violations: tuple[ViolationDetail, ...] | None = await engine.get_data(
                plate_info
            )
            if violations is None:
                continue
            logger.info(
                f"Plate {plate_info.plate}: Failed to get data with API: {api.value}..."
            )
            logger.info(
                f"Plate {plate_info.plate}: Sucessfully got data with API: {api.value}..."
            )
            self._plate_details.add(
                PlateDetail(
                    plate_info=plate_info,
                    violations=tuple(
                        violation for violation in violations if violation.status
                    )
                    if config.pending_fines_only
                    else violations,
                )
            )
            return
        logger.error(f"Plate {plate_info.plate}: Failed to get data!!!")

    async def get_data(self) -> tuple[PlateDetail, ...]:
        async with (
            CheckPhatNguoiGetDataEngine(
                timeout=config.request_timeout,
            ) as self._checkphatnguoi_engine,
            CsgtGetDataEngine(
                timeout=config.request_timeout,
            ) as self._csgt_engine,
            PhatNguoiGetDataEngine(
                timeout=config.request_timeout,
            ) as self._phatnguoi_engine,
            ZMIOGetDataEngine(timeout=config.request_timeout) as self._zmio_engine,
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
        return tuple(self._plate_details)
