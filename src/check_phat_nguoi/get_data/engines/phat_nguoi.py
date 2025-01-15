from __future__ import annotations

import re
from asyncio import TimeoutError
from datetime import datetime
from logging import getLogger
from re import DOTALL
from typing import override

from aiohttp import ClientError
from bs4 import BeautifulSoup, ResultSet, Tag

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import API_URL_PHATNGUOI as API_URL
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.context import PlateDetail, ViolationDetail
from check_phat_nguoi.types import ApiEnum, get_vehicle_enum
from check_phat_nguoi.utils import HttpaioSession

from .base import BaseGetDataEngine

logger = getLogger(__name__)


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
            any(
                v is None
                for v in (
                    plate,
                    color,
                    date,
                    location,
                    violation,
                    status,
                    enforcement_unit,
                )
            )
            or not resolution_offices
        ):
            logger.error(f"Plate {self._plate_info.plate}: Cannot parse the data")
            return
        # # TODO: Split resolution_office as other api
        self._violations_details_set.add(
            ViolationDetail(
                plate=plate,
                color=color,
                type=get_vehicle_enum(type),
                location=location,
                # Have to cast to string because lsp's warning
                date=datetime.strptime(str(date), DATETIME_FORMAT),
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
            return
        violation_htmls: ResultSet[Tag] | None = soup.css.select("tbody")
        if not violation_htmls:
            return
        for violation_html in violation_htmls:
            self._parse_violation(violation_html)
        return tuple(self._violations_details_set)


class PhatNguoiGetDataEngine(HttpaioSession, BaseGetDataEngine):
    api: ApiEnum = ApiEnum.phatnguoi_vn

    def __init__(self) -> None:
        HttpaioSession.__init__(self)

    async def _request(self, plate_info: PlateInfo) -> str | None:
        url: str = f"{API_URL}/{plate_info.plate}/{get_vehicle_enum(plate_info.type)}"
        try:
            async with self._session.get(url=url) as response:
                html_data: str = await response.text()
            return html_data
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
        html_data: str | None = await self._request(plate_info)
        if not html_data:
            return
        return PlateDetail(
            plate=plate_info.plate,
            owner=plate_info.owner,
            type=get_vehicle_enum(plate_info.type),
            violations=_PhatNguoiGetDataParseEngine(
                plate_info=plate_info,
                html_data=html_data,
            ).parse(),
        )

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)
