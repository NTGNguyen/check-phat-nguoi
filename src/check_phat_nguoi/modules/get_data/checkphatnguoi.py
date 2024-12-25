from datetime import datetime
from logging import getLogger
from threading import Thread
from typing import Dict, override

import requests
from requests import Response

from check_phat_nguoi.models.context.plate_context.plate_info import (
    PlateInfoContextModel,
)
from check_phat_nguoi.models.context.plate_context.violation import (
    ViolationContextModel,
)
from check_phat_nguoi.models.plate_info import PlateInfoModel
from check_phat_nguoi.modules.get_data.get_data_base import GetDataBase
from check_phat_nguoi.utils.constants import (
    DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT,
)
from check_phat_nguoi.utils.constants import GET_DATA_API_URL_CHECKPHATNGUOI as API_URL

logger = getLogger(__name__)


class GetDataCheckPhatNguoi(GetDataBase):
    def __init__(self, plate_infos: list[PlateInfoModel]) -> None:
        super().__init__(plate_infos)
        self.data_dict: Dict[str, None | Dict] = {}

    def _get_data_request(self, plate: str, timeout: int = 5) -> None:
        payload: dict[str, str] = {"bienso": f"{plate}"}
        try:
            response: Response = requests.post(
                url=API_URL, json=payload, timeout=timeout
            )
            response.raise_for_status()
            logger.info(f"Request successful: {response.status_code}")
            response_data: Dict = response.json()
            self.data_dict[plate] = response_data
        except requests.exceptions.ConnectionError:
            logger.error(f"Unable to connect to {API_URL}")
        except requests.exceptions.Timeout:
            logger.error(f"Time out of {timeout} seconds from URL {API_URL}")

    def _multi_thread_get_data(self) -> None:
        threads: list[Thread] = []
        for plate_info in self._plate_infos:
            thread = Thread(target=self._get_data_request, args=(plate_info.plate))
            threads.append(thread)
            thread.start()
        for idx, thread in enumerate(threads, start=1):
            try:
                thread.join()
            except Exception:
                logger.error(f"An error occurs in thread number {idx}")

    @staticmethod
    def get_plate_violation(
        plate_violation_dict: Dict | None,
    ) -> list[ViolationContextModel]:
        if plate_violation_dict is None:
            return []

        def _create_violation_model(data: Dict):
            return ViolationContextModel(
                type=data["Loại phương tiện"],
                date=datetime.strptime(data["Thời gian vi phạm"], DATETIME_FORMAT),
                location=data["Địa điểm vi phạm"],
                action=data["Hành vi vi phạm"],
                status=data["Trạng thái"],
                enforcement_unit=data["Đơn vị phát hiện vi phạm"],
                resolution_office=data["Nơi giải quyết vụ việc"],
            )

        return [
            _create_violation_model(violation_info_dict)
            for violation_info_dict in plate_violation_dict["data"]
        ]

    @override
    def get_data(self) -> list[PlateInfoContextModel]:
        self._multi_thread_get_data()
        plate_infos: list[PlateInfoContextModel] = [
            PlateInfoContextModel(
                plate=plate,
                violation=GetDataCheckPhatNguoi.get_plate_violation(
                    plate_violation_dict=plate_violation_dict
                ),
            )
            for plate, plate_violation_dict in self.data_dict.items()
        ]
        return plate_infos
