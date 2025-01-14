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


class CheckPhatNguoiGetDataEngine(BaseGetDataEngine, HttpaioSession):
    api: ApiEnum = ApiEnum.checkphatnguoi_vn
    headers: Final[dict[str, str]] = {"Content-Type": "application/json"}

    def __init__(self) -> None:
        HttpaioSession.__init__(self, headers=self.headers)

    @staticmethod
    def get_violations(
        plate_detail_dict: dict | None, filter_type: VehicleTypeEnum
    ) -> tuple[ViolationDetail, ...] | None:
        violations_details_set: set[ViolationDetail] = set()
        if not plate_detail_dict or not plate_detail_dict["data"]:
            return

        def _get_violation_detail(violation_dict: dict) -> None:
            type: VehicleStrVieType = violation_dict["Loại phương tiện"]
            # NOTE: this is for filtering the vehicle that doesn't match the plate info type. Because checkphatnguoi.vn return all of the type of the plate
            if get_vehicle_enum(type) != filter_type:
                return
            date: str = violation_dict["Thời gian vi phạm"]
            color: str = violation_dict["Màu biển"]
            location: str = violation_dict["Địa điểm vi phạm"]
            violation: str = violation_dict["Hành vi vi phạm"]
            status: bool = (
                False if violation_dict["Trạng thái"] == "Chưa xử phạt" else True
            )
            enforcement_unit: str = violation_dict["Đơn vị phát hiện vi phạm"]
            resolution_office: tuple[str, ...] = violation_dict[
                "Nơi giải quyết vụ việc"
            ]
            violation_detail: ViolationDetail = ViolationDetail(
                color=color,
                date=datetime.strptime(date, DATETIME_FORMAT),
                location=location,
                violation=violation,
                status=status,
                enforcement_unit=enforcement_unit,
                resolution_offices_details=resolution_office,
            )
            violations_details_set.add(violation_detail)

        for violation_dict in plate_detail_dict["data"]:
            _get_violation_detail(violation_dict)
        return tuple(violations_details_set)

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
            violations=self.get_violations(plate_detail_dict, type),
        )
