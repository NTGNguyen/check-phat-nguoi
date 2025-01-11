from __future__ import annotations

from datetime import datetime
from http.cookies import SimpleCookie
from io import BytesIO
from logging import getLogger
from ssl import SSLContext
from ssl import create_default_context as ssl_create_context
from typing import Final, override

from aiohttp import ClientError, ClientSession
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from PIL import Image
from pytesseract import image_to_string

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.constants import API_URL_CSGT_CAPTCHA as API_CAPTCHA
from check_phat_nguoi.constants import API_URL_CSGT_QUERY as API_QUERY
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.context import PlateDetail, ViolationDetail
from check_phat_nguoi.types import ApiEnum, VehicleTypeEnum, get_vehicle_enum

from .base import BaseGetDataEngine

logger = getLogger(__name__)


# https://github.com/PyGithub/PyGithub/issues/2300
SSL_CONTEXT: Final[SSLContext] = ssl_create_context()
SSL_CONTEXT.set_ciphers("DEFAULT@SECLEVEL=1")


class _GetDataCsgt:
    def __init__(self, plate_info: PlateInfo, *, session: ClientSession) -> None:
        self._plate_info: PlateInfo = plate_info
        self._session: ClientSession = session
        self._cookies: SimpleCookie
        self._captcha_img: bytes
        self._captcha: str

    @staticmethod
    def _bypass_captcha(captcha_img: bytes) -> str:
        with Image.open(BytesIO(captcha_img)) as image:
            return image_to_string(image).strip()

    async def _get_phpsessid_and_captcha(self) -> None:
        async with self._session.get(
            API_CAPTCHA,
            ssl=False,
        ) as response:
            response.raise_for_status()
            self._cookies = response.cookies
            self._captcha_img = await response.read()
            logger.debug(f"Plate {self._plate_info.plate} cookies: {self._cookies}")

    async def _get_html_data(self) -> str:
        await self._get_phpsessid_and_captcha()
        captcha: str = self._bypass_captcha(self._captcha_img)
        vehicle_type: VehicleTypeEnum = get_vehicle_enum(self._plate_info.type)
        payload: dict[str, str | int] = {
            "BienKS": self._plate_info.plate,
            "Xe": vehicle_type.value,
            "captcha": captcha,
            "ipClient": "9.9.9.91",
            "cUrl": vehicle_type.value,
        }
        headers: dict[str, str] = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with self._session.post(
            url=API_QUERY,
            headers=headers,
            cookies=self._cookies,
            data=payload,
            ssl=SSL_CONTEXT,
        ) as response:
            return await response.text()

    def _get_violations(
        self, violations_data: list[str]
    ) -> tuple[ViolationDetail, ...]:
        violations_details_set: set[ViolationDetail] = set()

        def _get_violation_detail(violation_data: str) -> None:
            soup: BeautifulSoup = BeautifulSoup(violation_data, "html.parser")
            if not soup.css:
                return
            forms: ResultSet[Tag] = soup.css.select(".form-group")
            date: str | None = (
                time_tag.text.strip()
                if (time_tag := forms[3].select_one("div.col-md-9"))
                else None
            )
            location: str | None = (
                location_tag.text.strip()
                if (location_tag := forms[4].select_one("div.col-md-9"))
                else None
            )
            violation: str | None = (
                action_tag.text.strip()
                if (action_tag := forms[5].select_one("div.col-md-9"))
                else None
            )
            status: str | None = (
                status_tag.text.strip()
                if (status_tag := forms[7].select_one("div.col-md-9"))
                else None
            )
            enforcement_unit: str | None = (
                status_tag.text.strip()
                if (status_tag := forms[8].select_one("div.col-md-9"))
                else None
            )
            resolution_offices_details: list[str] = [
                detail.text.strip() for detail in forms[9:]
            ]
            violation_detail: ViolationDetail = ViolationDetail(
                # Have to cast to string because lsp's warning
                date=datetime.strptime(str(date), DATETIME_FORMAT)
                if not date
                else None,
                location=location,
                violation=violation,
                status=False if status == "Chưa xử phạt" else True,
                enforcement_unit=enforcement_unit,
                resolution_offices_details=tuple(resolution_offices_details),
            )
            violations_details_set.add(violation_detail)

        for violation_data in violations_data:
            _get_violation_detail(violation_data)
        return tuple(violations_details_set)

    def _parse_html(self, html_data: str) -> PlateDetail | None:
        soup: BeautifulSoup = BeautifulSoup(html_data, "html.parser")
        violation_group_tag: Tag | NavigableString | None = soup.find(
            "div", id="bodyPrint123"
        )
        if not violation_group_tag or isinstance(violation_group_tag, NavigableString):
            return
        violation_group: str = violation_group_tag.prettify(formatter=None)
        violations_data: list[str] = "".join(violation_group.splitlines()[1:-2]).split(
            '<hr style="margin-bottom: 25px;"/>'
        )
        return PlateDetail(
            plate=self._plate_info.plate,
            owner=self._plate_info.owner,
            type=get_vehicle_enum(self._plate_info.type),
            violations=self._get_violations(violations_data),
        )

    async def get_data(self) -> PlateDetail | None:
        html_data: str = await self._get_html_data()
        if html_data == "404":
            logger.error(f"Plate {self._plate_info.plate}: Wrong captcha")
            return
        plate_detail: PlateDetail | None = self._parse_html(html_data)
        return plate_detail


class GetDataEngineCsgt(BaseGetDataEngine):
    api: ApiEnum = ApiEnum.csgt_vn

    @override
    async def get_data(self, plate_info: PlateInfo) -> PlateDetail | None:
        self.create_session()
        # NOTE: May never reach this condition because the session is created before this
        if not self._session:
            return
        get_data: _GetDataCsgt = _GetDataCsgt(plate_info, session=self._session)
        try:
            plate_detail: PlateDetail | None = await get_data.get_data()
            return plate_detail
        except TimeoutError as e:
            logger.error(
                f"Plate {plate_info.plate}: Time out ({self.timeout}s) getting data from API {self.api.value}\n{e}"
            )
        except (ClientError, Exception) as e:
            logger.error(
                f"Plate {plate_info.plate}: Error occurs while getting data from API {self.api.value}\n{e}"
            )
