from __future__ import annotations

import json
from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from typing import Final, override

from aiohttp import ClientError

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.constants import (
    GET_DATA_API_URL_CHECKPHATNGUOI as API_URL,
)
from check_phat_nguoi.context import (
    ViolationDetail,
)
from check_phat_nguoi.context.plates import PlateDetail
from check_phat_nguoi.types import (
    ApiEnum,
    VehicleStrVieType,
    VehicleTypeEnum,
    get_vehicle_enum,
)
from check_phat_nguoi.utils import HttpaioSession

from .base import BaseGetDataEngine

logger = getLogger(__name__)


class _CheckPhatNguoiGetDataParseEngine:
    def __init__(self, plate_info: PlateInfo, plate_detail_dict: dict) -> None:
        self._plate_info: PlateInfo = plate_info
        self._plate_detail_dict: dict = plate_detail_dict
        self._violations_details_set: set[ViolationDetail] = set()

    def _parse_violation(self, violation_dict: dict) -> None:
        type: VehicleStrVieType | None = violation_dict["Loại phương tiện"]
        # NOTE: this is for filtering the vehicle that doesn't match the plate info type. Because checkphatnguoi.vn return all of the type of the plate
        parsed_type: VehicleTypeEnum = get_vehicle_enum(type)
        if parsed_type != self._plate_info.type:
            return
        plate: str | None = violation_dict["Biển kiểm soát"]
        date: str | None = violation_dict["Thời gian vi phạm"]
        color: str | None = violation_dict["Màu biển"]
        location: str | None = violation_dict["Địa điểm vi phạm"]
        violation: str | None = violation_dict["Hành vi vi phạm"]
        status: str | None = violation_dict["Trạng thái"]
        enforcement_unit: str | None = violation_dict["Đơn vị phát hiện vi phạm"]
        resolution_offices: tuple[str, ...] | None = violation_dict[
            "Nơi giải quyết vụ việc"
        ]
        if any(
            v is None
            for v in (
                plate,
                color,
                date,
                location,
                violation,
                status,
                enforcement_unit,
                resolution_offices,
            )
        ):
            logger.error(f"Plate {self._plate_info.plate}: Cannot parse the data")
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

    def parse_violations(self) -> tuple[ViolationDetail, ...] | None:
        if not self._plate_detail_dict or not self._plate_detail_dict["data"]:
            return
        for violation_dict in self._plate_detail_dict["data"]:
            self._parse_violation(violation_dict)
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
        plate_detail_dict: dict | None = await self._request(plate_info)
        if not plate_detail_dict:
            return
        type: VehicleTypeEnum = get_vehicle_enum(plate_info.type)
        return PlateDetail(
            plate=plate_info.plate,
            owner=plate_info.owner,
            type=type,
            violations=_CheckPhatNguoiGetDataParseEngine(
                plate_info=plate_info, plate_detail_dict=plate_detail_dict
            ).parse_violations(),
        )

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)
