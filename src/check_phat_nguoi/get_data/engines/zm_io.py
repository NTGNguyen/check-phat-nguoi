from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from typing import Literal, TypedDict, cast, override

from aiohttp import ClientError

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import API_URL_ZM_IO
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.context import PlateDetail, ViolationDetail
from check_phat_nguoi.types import (
    ApiEnum,
    VehicleTypeEnum,
    get_vehicle_enum,
)
from check_phat_nguoi.utils import HttpaioSession

from .base import BaseGetDataEngine

logger = getLogger(__name__)


class _DataResponse(TypedDict):
    bienkiemsoat: str
    maubien: str
    loaiphuongtien: Literal["Ô tô", "Xe máy", "Xe máy điện"]
    thoigianvipham: str
    diadiemvipham: str
    trangthai: str
    donviphathienvipham: str
    noigiaiquyetvuviec: str


class _Response(TypedDict):
    json: tuple[_DataResponse, ...] | None
    html: str
    css: str


class _ZMIOGetDataParseEngine:
    def __init__(self, plate_info: PlateInfo, plate_detail_dict: _Response) -> None:
        self._plate_info: PlateInfo = plate_info
        self._plate_detail_typed: _Response = plate_detail_dict
        self._violations_details_set: set[ViolationDetail] = set()

    def _parse_violation(self, data: _DataResponse) -> None:
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
            date=datetime.strptime(str(date), DATETIME_FORMAT),
            location=location,
            status=status == "Đã xử phạt",
            enforcement_unit=enforcement_unit,
            resolution_offices=resolution_offices,
        )
        self._violations_details_set.add(violation_detail)

    def parse(self) -> tuple[ViolationDetail, ...] | None:
        if not self._plate_detail_typed["json"]:
            return
        for data in self._plate_detail_typed["json"]:
            self._parse_violation(data)
        return tuple(self._violations_details_set)


class ZMIOGetDataEngine(HttpaioSession, BaseGetDataEngine):
    api = ApiEnum.zm_io_vn

    def __init__(self):
        HttpaioSession.__init__(self)

    async def _request(self, plate_info: PlateInfo) -> dict | None:
        url = f"{API_URL_ZM_IO}?licensePlate={plate_info.plate}&vehicleType={get_vehicle_enum(plate_info.type)}"
        try:
            async with self._session.get(url) as response:
                json = await response.json()
                return json["data"]
        except TimeoutError as e:
            logger.error(
                f"Plate {plate_info.plate}: Time out ({self.timeout}s) getting data from API {self.api.value}. {e}"
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
    async def get_data(self, plate_info: PlateInfo) -> PlateDetail | None:
        plate_detail_raw: dict | None = await self._request(plate_info)
        if not plate_detail_raw:
            return
        plate_detail_typed: _Response = cast(_Response, plate_detail_raw)
        type: VehicleTypeEnum = get_vehicle_enum(plate_info.type)
        return PlateDetail(
            plate=plate_info.plate,
            owner=plate_info.owner,
            type=type,
            violations=_ZMIOGetDataParseEngine(
                plate_info=plate_info, plate_detail_dict=plate_detail_typed
            ).parse(),
        )

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)
