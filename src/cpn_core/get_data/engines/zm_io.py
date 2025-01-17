from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from typing import Literal, LiteralString, TypedDict, cast, override

from aiohttp import ClientError, ClientSession
from aiohttp.client import ClientTimeout

from cpn_core.get_data.engines.base import BaseGetDataEngine
from cpn_core.models.plate_info import PlateInfo
from cpn_core.models.violation_detail import ViolationDetail
from cpn_core.types.api import ApiEnum
from cpn_core.types.vehicle_type import get_vehicle_enum

logger = getLogger(__name__)

RESPONSE_DATETIME_FORMAT: LiteralString = "%H:%M, %d/%m/%Y"
API_URL: LiteralString = (
    "https://api.zm.io.vn/v1/csgt/tracuu?licensePlate={plate}&vehicleType={type}"
)


class _DataPlateInfoResponse(TypedDict):
    bienkiemsoat: str
    maubien: str
    loaiphuongtien: Literal["Ô tô", "Xe máy", "Xe máy điện"]
    thoigianvipham: str
    diadiemvipham: str
    trangthai: str
    donviphathienvipham: str
    noigiaiquyetvuviec: str


class _DataResponse(TypedDict):
    json: tuple[_DataPlateInfoResponse, ...] | None
    html: str
    css: str


class _Response(TypedDict):
    time_end: int
    data: _DataResponse
    error: bool


class _ZMIOGetDataParseEngine:
    def __init__(
        self,
        plate_info: PlateInfo,
        data: tuple[_DataPlateInfoResponse, ...],
    ) -> None:
        self._plate_info: PlateInfo = plate_info
        self._data: tuple[_DataPlateInfoResponse, ...] = data
        self._violations_details_set: set[ViolationDetail] = set()

    def _parse_violation(self, data: _DataPlateInfoResponse) -> None:
        plate: str = data["bienkiemsoat"]
        date: str = data["thoigianvipham"]
        type: Literal["Ô tô", "Xe máy", "Xe máy điện"] = data["loaiphuongtien"]
        color: str = data["maubien"]
        location: str = data["diadiemvipham"]
        status: str = data["trangthai"]
        enforcement_unit: str = data["donviphathienvipham"]
        # NOTE: this api just responses 1 resolution_office
        resolution_offices: tuple[str, ...] = (data["noigiaiquyetvuviec"],)
        violation_detail: ViolationDetail = ViolationDetail(
            plate=plate,
            color=color,
            type=get_vehicle_enum(type),
            date=datetime.strptime(str(date), RESPONSE_DATETIME_FORMAT),
            location=location,
            status=status == "Đã xử phạt",
            enforcement_unit=enforcement_unit,
            resolution_offices=resolution_offices,
            violation=None,
        )
        self._violations_details_set.add(violation_detail)

    def parse(self) -> tuple[ViolationDetail, ...] | None:
        for violations in self._data:
            self._parse_violation(violations)
        return tuple(self._violations_details_set)


class ZMIOGetDataEngine(BaseGetDataEngine):
    api = ApiEnum.zm_io_vn

    def __init__(self, *, timeout: float) -> None:
        self._timeout: float = timeout
        self._session: ClientSession = ClientSession(
            timeout=ClientTimeout(timeout),
        )

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self._session.close()

    async def _request(self, plate_info: PlateInfo) -> dict | None:
        url: str = API_URL.format(
            plate=plate_info.plate, type=get_vehicle_enum(plate_info.type)
        )
        try:
            async with self._session.get(url) as response:
                json: dict = await response.json()
                return json
        except TimeoutError as e:
            logger.error(
                f"Plate {plate_info.plate}: Time out ({self._timeout}s) getting data from API {self.api.value}. {e}"
            )
        except ClientError as e:
            logger.error(
                f"Plate {plate_info.plate}: Error occurs while getting data from API {self.api.value}. {e}"
            )
        except Exception as e:
            logger.error(
                f"Plate {plate_info.plate}: Error occurs while getting data (internally) {self.api.value}. {e}"
            )

    @override
    async def get_data(
        self, plate_info: PlateInfo
    ) -> tuple[ViolationDetail, ...] | None:
        plate_detail_raw: dict | None = await self._request(plate_info)
        if not plate_detail_raw:
            return
        plate_detail_typed: _Response = cast(_Response, plate_detail_raw)
        if plate_detail_typed["data"] is None:
            logger.error(f"Plate {plate_info.plate}: Cannot get data")
            return
        if plate_detail_typed["data"]["json"] is None:
            logger.info(
                f"Plate {plate_info.plate}: Not found or don't have any violations"
            )
            return ()
        violation_details: tuple[ViolationDetail, ...] | None = _ZMIOGetDataParseEngine(
            plate_info=plate_info, data=plate_detail_typed["data"]["json"]
        ).parse()
        return violation_details
