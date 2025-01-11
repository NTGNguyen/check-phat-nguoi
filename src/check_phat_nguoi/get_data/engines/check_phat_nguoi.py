from __future__ import annotations

import json
import re
from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from typing import Dict, Final, override

from aiohttp import ClientError

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.constants import (
    GET_DATA_API_URL_CHECKPHATNGUOI as API_URL,
)
from check_phat_nguoi.constants import OFFICE_NAME_PATTERN
from check_phat_nguoi.context import (
    ResolutionOffice,
    Violation,
)
from check_phat_nguoi.context.plates.models.plate_detail import PlateDetail
from check_phat_nguoi.types import get_vehicle_enum

from .base import BaseGetDataEngine

logger = getLogger(__name__)


class GetDataEngineCheckPhatNguoi(BaseGetDataEngine):
    headers: Final[dict[str, str]] = {"Content-Type": "application/json"}

    def __init__(self) -> None:
        super().__init__(session_header=self.headers)

    async def _get_data_request(self, plate_info: PlateInfo) -> Dict | None:
        payload: Final[dict[str, str]] = {"bienso": plate_info.plate}
        try:
            async with self.session.post(
                API_URL,
                json=payload,
            ) as response:
                response.raise_for_status()
                response_data = await response.read()
                logger.info(f"Plate {plate_info.plate}: Get data successfully")
                return json.loads(response_data)
        # TODO: Show API enum instead of URL
        except TimeoutError as e:
            logger.error(
                f"Plate {plate_info.plate}: Time out ({self.timeout}s) getting data from API {API_URL}\n{e}"
            )
        except (ClientError, Exception) as e:
            logger.error(
                f"Plate {plate_info.plate}: Error occurs while getting data from API {API_URL}\n{e}"
            )

    @override
    async def get_data(self, plate_info: PlateInfo) -> PlateDetail | None:
        plate_data: Dict | None = await self._get_data_request(plate_info)
        if plate_data is None:
            return
        return PlateDetail(
            plate=plate_info.plate,
            owner=plate_info.owner,
            type=get_vehicle_enum(plate_info.type),
            violation=self.get_plate_violation(plate_data),
        )

    @staticmethod
    def get_plate_violation(
        plate_violation_dict: Dict | None,
    ) -> tuple[Violation, ...]:
        if plate_violation_dict is None:
            return ()
        if plate_violation_dict["data"] is None:
            return ()

        # FIXME: please unwrap us @NTGNguyen huhu

        def _create_resolution_office_mode(
            resolution_offices: list[str],
        ) -> tuple[ResolutionOffice, ...]:
            parsed_office_dict: Dict[str, Dict] = {}
            current_name = None
            # FIXME: Declare Type for typesafety, use ResolutionOfficeModel
            for office_info in resolution_offices:
                if re.match(OFFICE_NAME_PATTERN, office_info):
                    current_name = office_info.split(".", 1)[1].strip()
                    parsed_office_dict[current_name] = {"Address": None, "Phone": None}
                elif "Địa chỉ" in office_info:
                    if current_name:
                        parsed_office_dict[current_name]["Address"] = office_info.split(
                            ":", 1
                        )[1].strip()
                elif "Số điện thoại" in office_info:
                    if current_name:
                        parsed_office_dict[current_name]["Phone"] = office_info.split(
                            ":", 1
                        )[1].strip()

            return tuple(
                ResolutionOffice(
                    location_name=location_name,
                    address=location_detail["Address"],
                    phone=location_detail["Phone"],
                )
                for location_name, location_detail in parsed_office_dict.items()
            )

        def _create_violation_model(data: Dict):
            return Violation(
                type=data["Loại phương tiện"],
                date=datetime.strptime(data["Thời gian vi phạm"], DATETIME_FORMAT),
                location=data["Địa điểm vi phạm"],
                action=data["Hành vi vi phạm"],
                status=False if data["Trạng thái"] == "Chưa xử phạt" else True,
                enforcement_unit=data["Đơn vị phát hiện vi phạm"],
                resolution_office=_create_resolution_office_mode(
                    data["Nơi giải quyết vụ việc"]
                ),
            )

        return tuple(
            _create_violation_model(violation_info_dict)
            for violation_info_dict in plate_violation_dict["data"]
        )
