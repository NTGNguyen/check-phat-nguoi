from datetime import datetime
from http.cookies import SimpleCookie
from io import BytesIO
from logging import getLogger
from ssl import SSLContext
from ssl import create_default_context as ssl_create_context
from typing import Final, LiteralString, override

from aiohttp import ClientError
from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image
from pytesseract import image_to_string

from cpn_core.models import PlateInfo, ViolationDetail
from cpn_core.types import ApiEnum, VehicleTypeEnum, get_vehicle_enum
from cpn_core.utils import HttpaioSession

from ..exceptions import GetDataError, ParseDataError
from .base import BaseGetDataEngine

RESPONSE_DATETIME_FORMAT: LiteralString = "%H:%M, %d/%m/%Y"

API_CAPTCHA: LiteralString = "https://www.csgt.vn/lib/captcha/captcha.class.php"
API_QUERY_1: LiteralString = "https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax"
API_QUERY_2: LiteralString = "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html?&LoaiXe={vehicle_type}&BienKiemSoat={plate}"

logger = getLogger(__name__)


# https://github.com/PyGithub/PyGithub/issues/2300
SSL_CONTEXT: Final[SSLContext] = ssl_create_context()
SSL_CONTEXT.set_ciphers("DEFAULT@SECLEVEL=1")


class _GetDataCsgtCoreEngine(HttpaioSession):
    api: ApiEnum = ApiEnum.csgt_vn

    def __init__(self, plate_info: PlateInfo) -> None:
        self._plate_info: PlateInfo = plate_info
        self._vehicle_type: VehicleTypeEnum = get_vehicle_enum(self._plate_info.type)
        HttpaioSession.__init__(self)
        self._violations_details_set: set[ViolationDetail] = set()

    @staticmethod
    def _bypass_captcha(captcha_img: bytes) -> str:
        with Image.open(BytesIO(captcha_img)) as image:
            return image_to_string(image).strip()

    async def _get_phpsessid_and_captcha(self) -> tuple[str, bytes]:
        logger.debug(f"Plate {self._plate_info.plate}: Getting cookies and captcha...")
        async with self._session.get(
            API_CAPTCHA,
            ssl=SSL_CONTEXT,
        ) as response:
            response.raise_for_status()
            phpsessid: str = response.cookies["PHPSESSID"].value
            captcha_img: bytes = await response.read()
            logger.debug(f"Plate {self._plate_info.plate} PHPSESSID: {phpsessid}")
            return phpsessid, captcha_img

    async def _get_html_check(self, captcha: str, phpsessid: str) -> str:
        payload: dict[str, str | int] = {
            "BienKS": self._plate_info.plate,
            "Xe": self._vehicle_type.value,
            "captcha": captcha,
            "ipClient": "9.9.9.91",
            "cUrl": self._vehicle_type.value,
        }
        headers: dict[str, str] = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        cookies: SimpleCookie = SimpleCookie(f"PHPSESSID={phpsessid}")
        async with self._session.post(
            url=API_QUERY_1,
            headers=headers,
            cookies=cookies,
            data=payload,
            ssl=SSL_CONTEXT,
        ) as response:
            return await response.text()

    async def _get_plate_data(self) -> str:
        async with self._session.post(
            url=API_QUERY_2.format(
                vehicle_type=self._vehicle_type.value,
                plate=self._plate_info.plate,
            ),
            ssl=SSL_CONTEXT,
        ) as response:
            return await response.text()

    def _parse_violation(self, violation_data: str) -> None:
        soup: BeautifulSoup = BeautifulSoup(violation_data, "html.parser")
        if not soup.css:
            return
        plate: str | None = (
            plate_tag.text.strip()
            if (
                plate_tag := soup.select_one(
                    ".form-group:nth-child(1) > div > div:nth-child(2)"
                )
            )
            else None
        )
        color: str | None = (
            color_tag.text.strip()
            if (
                color_tag := soup.select_one(
                    ".form-group:nth-child(2) > div > div:nth-child(2)"
                )
            )
            else None
        )
        type: str | None = (
            type_tag.text.strip()
            if (
                type_tag := soup.select_one(
                    ".form-group:nth-child(3) > div > div:nth-child(2)"
                )
            )
            else None
        )
        date: str | None = (
            date_tag.text.strip()
            if (
                date_tag := soup.select_one(
                    ".form-group:nth-child(4) > div > div:nth-child(2)"
                )
            )
            else None
        )
        location: str | None = (
            location_tag.text.strip()
            if (
                location_tag := soup.select_one(
                    ".form-group:nth-child(5) > div > div:nth-child(2)"
                )
            )
            else None
        )
        violation: str | None = (
            action_tag.text.strip()
            if (
                action_tag := soup.select_one(
                    ".form-group:nth-child(6) > div > div:nth-child(2)"
                )
            )
            else None
        )
        status: str | None = (
            status_tag.text.strip()
            if (
                status_tag := soup.select_one(
                    ".form-group:nth-child(7) > div > div:nth-child(2)"
                )
            )
            else None
        )
        enforcement_unit: str | None = (
            enforcement_unit_tag.text.strip()
            if (
                enforcement_unit_tag := soup.select_one(
                    ".form-group:nth-child(8) > div > div:nth-child(2)"
                )
            )
            else None
        )
        resolution_offices: list[str] = [
            resolution_offices_tag.text.strip()
            for resolution_offices_tag in soup.select(".form-group:nth-child(n+9)")
        ]
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
        violation_detail: ViolationDetail = ViolationDetail(
            plate=plate,
            color=color,
            type=get_vehicle_enum(type),
            # Have to cast to string because lsp's warning
            date=datetime.strptime(str(date), RESPONSE_DATETIME_FORMAT),
            location=location,
            violation=violation,
            status=status == "Đã xử phạt",
            enforcement_unit=enforcement_unit,
            resolution_offices=tuple(resolution_offices),
        )
        self._violations_details_set.add(violation_detail)

    def _parse_violations(
        self, violations_data: list[str]
    ) -> tuple[ViolationDetail, ...]:
        for violation_data in violations_data:
            self._parse_violation(violation_data)
        if len(self._violations_details_set) == 0:
            raise ParseDataError("Cannot get violations data")
        return tuple(self._violations_details_set)

    def _parse_html(self, html: str) -> tuple[ViolationDetail, ...]:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        violation_group_tag: Tag | NavigableString | None = soup.find(
            "div", id="bodyPrint123"
        )
        if not violation_group_tag or isinstance(violation_group_tag, NavigableString):
            raise ParseDataError('"Cannot get the div whose id is "bodyPrint123"')
        violation_group: str = violation_group_tag.prettify(formatter=None)
        # HACK: This split is hard. Maybe change it to regex split later
        violations_data: list[str] = "".join(violation_group.splitlines()[1:-2]).split(
            '<hr style="margin-bottom: 25px;"/>'
        )
        return self._parse_violations(violations_data)

    async def get_data(self) -> tuple[ViolationDetail, ...]:
        try:
            phpsessid, captcha_img = await self._get_phpsessid_and_captcha()
            captcha: str = self._bypass_captcha(captcha_img)
            logger.debug(f"Plate {self._plate_info.plate} captcha resolved: {captcha}")
            logger.debug(
                f"Plate {self._plate_info.plate}: Sending request again to get check..."
            )
            html_data: str = await self._get_html_check(captcha, phpsessid)
            if html_data.strip() == "404":
                logger.error(f"Plate {self._plate_info.plate}: Wrong captcha")
                raise GetDataError("Wrong captcha")
            logger.debug(
                f"Plate {self._plate_info.plate}: Sending request again to get data..."
            )
            # FIXME: try to handle the request raise
            plate_data: str = await self._get_plate_data()
            violations: tuple[ViolationDetail, ...] = self._parse_html(plate_data)
            return violations
        except TimeoutError as e:
            logger.error(
                f"Plate {self._plate_info.plate}: Time out ({self.timeout}s) getting data from API {self.api.value}. {e}"
            )
            raise
        except ClientError as e:
            logger.error(
                f"Plate {self._plate_info.plate}: Error occurs while getting data from API {self.api.value}. {e}"
            )
            raise
        except Exception as e:
            logger.error(
                f"Plate {self._plate_info.plate}: Error occurs while getting data (internally) {self.api.value}. {e}"
            )
            raise

    @override
    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        return await HttpaioSession.__aexit__(self, exc_type, exc_value, exc_traceback)


class CsgtGetDataEngine(BaseGetDataEngine):
    @override
    async def get_data(self, plate_info: PlateInfo) -> tuple[ViolationDetail, ...]:
        async with _GetDataCsgtCoreEngine(plate_info) as local_engine:
            return await local_engine.get_data()
