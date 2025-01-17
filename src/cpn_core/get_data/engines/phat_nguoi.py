import re
from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from re import DOTALL
from typing import LiteralString, override

from aiohttp import ClientError, ClientSession, ClientTimeout
from bs4 import BeautifulSoup, ResultSet, Tag

from cpn_core.get_data.engines.base import BaseGetDataEngine
from cpn_core.models.plate_info import PlateInfo
from cpn_core.models.violation_detail import ViolationDetail
from cpn_core.types.api import ApiEnum
from cpn_core.types.vehicle_type import (
    get_vehicle_enum,
)

logger = getLogger(__name__)

API_URL: LiteralString = "https://api.phatnguoi.vn/web/tra-cuu"
RESPONSE_DATETIME_FORMAT: LiteralString = "%H:%M, %d/%m/%Y"


class _PhatNguoiGetDataParseEngine:
    def __init__(self, plate_info: PlateInfo, html_data: str) -> None:
        self._plate_info: PlateInfo = plate_info
        self._html_data: str = html_data
        self._violations_details_set: set[ViolationDetail] = set()

    def _parse_violation(self, violation_html: Tag) -> None:
        plate: str | None = (
            plate_tag.text.strip()
            if (
                plate_tag := violation_html.select_one(
                    "tr:nth-child(1) > td:nth-child(2)"
                )
            )
            else None
        )
        color: str | None = (
            color_tag.text.strip()
            if (
                color_tag := violation_html.select_one(
                    "tr:nth-child(2) > td:nth-child(2)"
                )
            )
            else None
        )
        type: str | None = (
            type_tag.text.strip()
            if (
                type_tag := violation_html.select_one(
                    "tr:nth-child(3) > td:nth-child(2)"
                )
            )
            else None
        )
        date: str | None = (
            date_tag.text.strip()
            if (
                date_tag := violation_html.select_one(
                    "tr:nth-child(4) > td:nth-child(2)"
                )
            )
            else None
        )
        location: str | None = (
            location_tag.text.strip()
            if (
                location_tag := violation_html.select_one(
                    "tr:nth-child(5) > td:nth-child(2)"
                )
            )
            else None
        )
        violation: str | None = (
            violation_tag.text.strip()
            if (
                violation_tag := violation_html.select_one(
                    "tr:nth-child(6) > td:nth-child(2)"
                )
            )
            else None
        )
        status: str | None = (
            status_tag.text.strip()
            if (
                status_tag := violation_html.select_one(
                    "tr:nth-child(7) > td:nth-child(2)"
                )
            )
            else None
        )
        enforcement_unit: str | None = (
            enforcement_unit_tag.text.strip()
            if (
                enforcement_unit_tag := violation_html.select_one(
                    "tr:nth-child(8) > td:nth-child(2)"
                )
            )
            else None
        )
        resolution_offices: str | None = (
            resolution_offices_tag.text.strip()
            if (
                resolution_offices_tag := violation_html.select_one(
                    "tr:nth-child(9) > td:nth-child(2)"
                )
            )
            else None
        )
        if (
            plate is None
            or color is None
            or date is None
            or location is None
            or violation is None
            or status is None
            or enforcement_unit is None
            or not resolution_offices
        ):
            logger.error(
                f"Plate {self._plate_info.plate}: Cannot parse a violation data"
            )
            return
        # # TODO: Split resolution_office as other api
        self._violations_details_set.add(
            ViolationDetail(
                plate=plate,
                color=color,
                type=get_vehicle_enum(type),
                location=location,
                # Have to cast to string because lsp's warning
                date=datetime.strptime(str(date), RESPONSE_DATETIME_FORMAT),
                violation=violation,
                status=status == "Đã xử phạt",
                enforcement_unit=enforcement_unit,
                resolution_offices=tuple(
                    re.findall(r"\d\..*?(?=(?:\d\.|$))", resolution_offices, DOTALL)
                ),
            )
        )

    def parse(self) -> tuple[ViolationDetail, ...] | None:
        soup: BeautifulSoup = BeautifulSoup(self._html_data, "html.parser")
        if not soup.css:
            logger.error("The data got doesn't have css selector ability")
            return
        violation_htmls: ResultSet[Tag] | None = soup.css.select("tbody")
        if not violation_htmls:
            logger.error("Cannot get the tbody tag")
            return
        for violation_html in violation_htmls:
            self._parse_violation(violation_html)
        violation_details: tuple[ViolationDetail, ...] = tuple(
            self._violations_details_set
        )
        if not violation_details:
            logger.info(f"Plate {self._plate_info.plate}: Don't find any violation")
        return violation_details


class PhatNguoiGetDataEngine(BaseGetDataEngine):
    api: ApiEnum = ApiEnum.phatnguoi_vn

    def __init__(self, *, timeout: float) -> None:
        self._timeout: float = timeout
        self._session: ClientSession = ClientSession(
            timeout=ClientTimeout(timeout),
        )

    async def _request(self, plate_info: PlateInfo) -> str | None:
        url: str = f"{API_URL}/{plate_info.plate}/{get_vehicle_enum(plate_info.type)}"
        try:
            async with self._session.get(url=url) as response:
                html_data: str = await response.text()
            return html_data
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
        html_data: str | None = await self._request(plate_info)
        if html_data is None:
            return
        violations: tuple[ViolationDetail, ...] | None = _PhatNguoiGetDataParseEngine(
            plate_info=plate_info,
            html_data=html_data,
        ).parse()
        return violations

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self._session.close()
