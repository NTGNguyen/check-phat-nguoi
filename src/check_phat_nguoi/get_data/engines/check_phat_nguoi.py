from __future__ import annotations

import json
from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from typing import Final, Literal, TypeAlias, TypedDict, cast, override

from aiohttp import ClientError

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.constants import (
    GET_DATA_API_URL_CHECKPHATNGUOI as API_URL,
)
from check_phat_nguoi.context import (
    PlateDetail,
    ViolationDetail,
)
from check_phat_nguoi.types import (
    ApiEnum,
    VehicleStrVieType,
    VehicleTypeEnum,
    get_vehicle_enum,
)
from check_phat_nguoi.utils import HttpaioSession

from .base import BaseGetDataEngine

logger = getLogger(__name__)

# HACK: Those type so bruh that's not really strict like Typescript. I love typescript btw

_DataResponse = TypedDict(
    "_DataResponse",
    {
        "Biển kiểm soát": str,
        "Màu biển": str,
        "Loại phương tiện": VehicleStrVieType,
        "Thời gian vi phạm": str,
        "Địa điểm vi phạm": str,
        "Hành vi vi phạm": str,
        "Trạng thái": str,
        "Đơn vị phát hiện vi phạm": str,
        "Nơi giải quyết vụ việc": tuple[str, ...],
    },
)

_DataPlateInfoResponse = TypedDict(
    "_DataPlateInfoResponse",
    {
        "total": int,
        "chuaxuphat": Literal[0, 1],
        "daxuphat": Literal[0, 1],
        "latest": str,
    },
)

_FoundResponse = TypedDict(
    "_FoundResponse",
    {
        "status": Literal[1],
        "msg": str,
        "data": tuple[_DataResponse, ...],
    },
)


_NotFoundResponse = TypedDict(
    "_NotFoundResponse",
    {
        "status": Literal[2],
        "data": None,
    },
)

_Response: TypeAlias = _FoundResponse | _NotFoundResponse


class _CheckPhatNguoiGetDataParseEngine:
    def __init__(self, plate_info: PlateInfo, plate_detail_dict: _Response) -> None:
        self._plate_info: PlateInfo = plate_info
        self._plate_detail_typed: _Response = plate_detail_dict
        self._violations_details_set: set[ViolationDetail] = set()

    def _parse_violation(self, data: _DataResponse) -> None:
        type: VehicleStrVieType | None = data["Loại phương tiện"]
        # NOTE: this is for filtering the vehicle that doesn't match the plate info type. Because checkphatnguoi.vn return all of the type of the plate
        parsed_type: VehicleTypeEnum = get_vehicle_enum(type)
        if parsed_type != self._plate_info.type:
            return
        plate: str = data["Biển kiểm soát"]
        date: str = data["Thời gian vi phạm"]
        color: str = data["Màu biển"]
        location: str = data["Địa điểm vi phạm"]
        violation: str = data["Hành vi vi phạm"]
        status: str = data["Trạng thái"]
        enforcement_unit: str = data["Đơn vị phát hiện vi phạm"]
        resolution_offices: tuple[str, ...] = data["Nơi giải quyết vụ việc"]
        violation_detail: ViolationDetail = ViolationDetail(
            plate=plate,
            color=color,
            type=parsed_type,
            # Have to cast to string because lsp's warning
            date=datetime.strptime(str(date), DATETIME_FORMAT),
            location=location,
            violation=violation,
            status=status == "Đã xử phạt",
            enforcement_unit=enforcement_unit,
            resolution_offices=resolution_offices,
        )
        self._violations_details_set.add(violation_detail)

    def parse(self) -> tuple[ViolationDetail, ...] | None:
        if self._plate_detail_typed["status"] != 1:
            return
        for data in self._plate_detail_typed["data"]:
            self._parse_violation(data)
        return tuple(self._violations_details_set)


class CheckPhatNguoiGetDataEngine(BaseGetDataEngine, HttpaioSession):
    api: ApiEnum = ApiEnum.checkphatnguoi_vn
    headers: Final[dict[str, str]] = {"Content-Type": "application/json"}

    def __init__(self) -> None:
        HttpaioSession.__init__(self, headers=self.headers)

    async def _request(self, plate_info: PlateInfo) -> dict | None:
        payload: Final[dict[str, str]] = {"bienso": plate_info.plate}
        try:
            async with self._session.post(
                API_URL,
                json=payload,
            ) as response:
                response.raise_for_status()
                response_data = await response.read()
                logger.info(f"Plate {plate_info.plate}: Get data successfully")
                return json.loads(response_data)
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
            violations=_CheckPhatNguoiGetDataParseEngine(
                plate_info=plate_info, plate_detail_dict=plate_detail_typed
            ).parse(),
        )

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)
