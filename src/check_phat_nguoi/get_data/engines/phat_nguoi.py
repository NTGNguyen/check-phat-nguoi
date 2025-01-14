from __future__ import annotations

import re
from asyncio import TimeoutError
from logging import getLogger
from re import DOTALL
from typing import override

from aiohttp import ClientError
from bs4 import BeautifulSoup, ResultSet

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import API_URL_PHATNGUOI
from check_phat_nguoi.context import PlateDetail
from check_phat_nguoi.context.plates import ViolationDetail
from check_phat_nguoi.types import ApiEnum, VehicleTypeEnum, get_vehicle_enum
from check_phat_nguoi.utils import HttpaioSession

from .base import BaseGetDataEngine

logger = getLogger(__name__)


class PhatNguoiGetDataEngine(HttpaioSession, BaseGetDataEngine):
    api: ApiEnum = ApiEnum.phatnguoi_vn

    def __init__(self) -> None:
        HttpaioSession.__init__(self)

    @staticmethod
    def get_violations(html: str):
        soup = BeautifulSoup(html, "html.parser")
        violation_htmls: ResultSet[BeautifulSoup] = soup.find_all("tbody")
        if violation_htmls is None:
            return
        violation_detail_set: set[ViolationDetail] = set()

        def _get_violation(violation_html: BeautifulSoup):
            details: ResultSet[BeautifulSoup] = violation_html.find_all("tr")
            color: ResultSet[BeautifulSoup] = details[1].find_all()
            color_detail: str = color[1].text
            location: ResultSet[BeautifulSoup] = details[4].find_all()
            location_detail: str = location[1].text.strip()
            action: ResultSet[BeautifulSoup] = details[5].find_all()
            action_detail: str = action[1].text.strip()
            status: ResultSet[BeautifulSoup] = details[6].find_all()
            status_detail: bool = (
                True if status[1].text.strip() == "ĐÃ XỬ PHẠT" else False
            )
            enforcement_unit: ResultSet[BeautifulSoup] = details[7].find_all()
            enforcement_unit_detail: str = enforcement_unit[1].text.strip()
            resolution_offices: ResultSet[BeautifulSoup] = details[8].find_all()
            resolution_office_details: str = resolution_offices[1].text.strip()
            # TODO: Split resolution_office as other api
            violation_detail_set.add(
                ViolationDetail(
                    color=color_detail,
                    location=location_detail,
                    violation=action_detail,
                    status=status_detail,
                    enforcement_unit=enforcement_unit_detail,
                    resolution_offices_details=tuple(
                        re.findall(
                            r"\d\..*?(?=(?:\d\.|$))", resolution_office_details, DOTALL
                        )
                    ),
                )
            )

        for violation_html in violation_htmls:
            _get_violation(violation_html)
        return tuple(violation_detail_set)

    async def _request(self, plate_info: PlateInfo) -> str | None:
        url: str = (
            f"{API_URL_PHATNGUOI}{plate_info.plate}/{get_vehicle_enum(plate_info.type)}"
        )
        try:
            async with self._session.get(url=url) as response:
                html = await response.text()
            return html
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
        html: str | None = await self._request(plate_info)
        if not html:
            return

        type: VehicleTypeEnum = get_vehicle_enum(plate_info.type)
        return PlateDetail(
            plate=plate_info.plate,
            owner=plate_info.owner,
            type=type,
            violations=self.get_violations(html),
        )

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)
