from asyncio import gather
from logging import getLogger

from aiohttp import ClientError

from cpn_cli.config_reader import config
from cpn_cli.models import PlateDetail
from cpn_core.get_data import GetDataError, ParseDataError
from cpn_core.get_data.engines.base import BaseGetDataEngine
from cpn_core.get_data.engines.check_phat_nguoi import CheckPhatNguoiGetDataEngine
from cpn_core.get_data.engines.csgt import CsgtGetDataEngine
from cpn_core.get_data.engines.phat_nguoi import PhatNguoiGetDataEngine
from cpn_core.models import PlateInfo, ViolationDetail
from cpn_core.types import ApiEnum

logger = getLogger(__name__)


class GetData:
    def __init__(self) -> None:
        self._checkphatnguoi_engine: CheckPhatNguoiGetDataEngine
        self._csgt_engine: CsgtGetDataEngine
        self._phatnguoi_engine: PhatNguoiGetDataEngine
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
            logger.info(
                f"Plate {plate_info.plate}: Getting data with API: {api.value}..."
            )
            try:
                violations: tuple[ViolationDetail, ...] = await engine.get_data(
                    plate_info
                )
            except TimeoutError as e:
                logger.error(
                    f"Plate {plate_info.plate}: Time out ({config.request_timeout}s) getting data from API {api.value}. {e}"
                )
                continue
            except ClientError as e:
                logger.error(
                    f"Plate {plate_info.plate}: Error occurs while getting data from API {api.value}. {e}"
                )
                continue
            except GetDataError as e:
                logger.error(
                    f"Plate {plate_info.plate} - {api.value}: Error while getting data. {e}"
                )
                continue
            except ParseDataError as e:
                logger.error(
                    f"Plate {plate_info.plate} - {api.value}: Error while parsing data. {e}"
                )
                continue
            except Exception as e:
                logger.error(
                    f"Plate {plate_info.plate}: Error occurs while getting data (internally) {api.value}. {e}"
                )
                continue
            logger.info(
                f"Plate {plate_info.plate}: Sucessfully got data with API: {api.value}..."
            )
            self._plate_details.add(
                PlateDetail(plate_info=plate_info, violations=violations)
            )
        logger.error(f"Plate {plate_info.plate}: Failed to get data!!!")

    async def get_data(self) -> tuple[PlateDetail, ...]:
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
        return tuple(self._plate_details)
