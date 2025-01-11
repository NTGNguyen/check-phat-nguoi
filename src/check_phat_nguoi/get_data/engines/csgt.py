from __future__ import annotations

from datetime import datetime
from http.cookies import SimpleCookie
from io import BytesIO
from logging import getLogger
from typing import Final, Self

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup, NavigableString
from PIL import Image
from pytesseract import image_to_string

from check_phat_nguoi.config import PlateInfo
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.constants import API_URL_CSGT_CAPTCHA as API_CAPTCHA
from check_phat_nguoi.constants import API_URL_CSGT_QUERY as API_QUERY
from check_phat_nguoi.constants import DATETIME_FORMAT_CHECKPHATNGUOI as DATETIME_FORMAT
from check_phat_nguoi.context import PlateDetail, Violation
from check_phat_nguoi.types import get_vehicle_enum

logger = getLogger(__name__)


class GetDataEngineCsgt:
    timeout: Final[int] = config.request_timeout
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self, plate: PlateInfo) -> None:
        self.plate: PlateInfo = plate
        self.session: ClientSession = ClientSession(
            timeout=ClientTimeout(self.timeout),
        )
        logger.debug(f"Created get data engine session: {type(self).__name__}")

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback) -> None:
        await self.session.close()
        logger.debug(f"Closed data engine session: {type(self).__name__}")

    def _bypass_captcha(self, captcha_img: bytes) -> str:
        with Image.open(BytesIO(captcha_img)) as image:
            return image_to_string(image).strip()

    async def _get_phpsessid_and_captcha(self) -> tuple[SimpleCookie, bytes]:
        async with self.session.get(API_CAPTCHA) as response:
            response.raise_for_status()
            cookies = response.cookies
            captcha_img = await response.read()
            return cookies, captcha_img

    async def _get_html_data_raw(self) -> str:
        cookies, captcha_img = await self._get_phpsessid_and_captcha()
        captcha: str = self._bypass_captcha(captcha_img)
        vehicle_type: int = get_vehicle_enum(self.plate.type)
        payload = {
            "BienKS": self.plate.plate,
            "Xe": vehicle_type,
            "captcha": captcha,
            "ipClient": "9.9.9.91",
            "cUrl": vehicle_type,
        }
        async with self.session.post(
            API_QUERY,
            headers=self.headers,
            cookies=cookies,
            data=payload,
        ) as response:
            return await response.text()

    def _get_violation(self, violation_text: str) -> Violation | None:
        type: str
        match get_vehicle_enum(self.plate.type):
            case 1:
                type = "Ô tô"
            case 2:
                type = "Xe máy"
            case _:
                type = "Xe đạp điện"
        vio_soup: BeautifulSoup = BeautifulSoup(violation_text, "html.parser")
        if not vio_soup.css:
            return
        divs = vio_soup.css.select(".form-group")
        time = (
            time_tag.text.strip()
            if (time_tag := divs[3].select_one("div.col-md-9"))
            else None
        )
        if not time:
            return
        location = (
            location_tag.text.strip()
            if (location_tag := divs[4].select_one("div.col-md-9"))
            else None
        )
        if not location:
            return
        action = (
            action_tag.text.strip()
            if (action_tag := divs[5].select_one("div.col-md-9"))
            else None
        )
        if not action:
            return
        status = (
            status_tag.text.strip()
            if (status_tag := divs[7].select_one("div.col-md-9"))
            else None
        )
        if not status:
            return
        don_vi_phat_hien = (
            status_tag.text.strip()
            if (status_tag := divs[8].select_one("div.col-md-9"))
            else None
        )
        if not don_vi_phat_hien:
            return
        resolve_details = [detail.text.strip() for detail in divs[9:]]
        return Violation(
            type=type,
            date=datetime.strptime(time, DATETIME_FORMAT),
            location=location,
            action=action,
            status=False if status == "Chưa xử phạt" else True,
            enforcement_unit=don_vi_phat_hien,
            resolution_office=tuple(resolve_details),
        )

    def _get_violations(self, violations_group: list[str]) -> tuple[Violation, ...]:
        violations_with_none = tuple(
            self._get_violation(violation_text) for violation_text in violations_group
        )
        return tuple(violation for violation in violations_with_none if violation)

    def _parse_html(self, html_content: str) -> PlateDetail | None:
        soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")
        violation_htmls = soup.find("div", id="bodyPrint123")
        if not violation_htmls or isinstance(violation_htmls, NavigableString):
            return
        violation_htmls_text = violation_htmls.prettify(formatter=None)
        violations_group: list[str] = "".join(
            violation_htmls_text.splitlines()[1:-2]
        ).split('<hr style="margin-bottom: 25px;"/>')
        return PlateDetail(
            plate=self.plate.plate,
            owner=self.plate.owner,
            type=get_vehicle_enum(self.plate.type),
            violation=tuple(self._get_violations(violations_group)),
        )

    async def get_data(
        self,
    ) -> PlateDetail | None:
        html_content = await self._get_html_data_raw()
        return self._parse_html(html_content)


# TODO: I will try catch later @KevinNitroG
