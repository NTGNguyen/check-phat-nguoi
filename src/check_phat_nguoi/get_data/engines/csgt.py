from __future__ import annotations

from http.cookies import SimpleCookie
from io import BytesIO
from logging import getLogger
from typing import Final, Self

from aiohttp import ClientSession, ClientTimeout
from PIL import Image
from pytesseract import image_to_string

from check_phat_nguoi.config import PlateInfoDTO
from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.constants import API_URL_CSGT_CAPTCHA as API_CAPTCHA
from check_phat_nguoi.constants import API_URL_CSGT_QUERY as API_QUERY
from check_phat_nguoi.context import PlateInfoModel
from check_phat_nguoi.types import get_vehicle_enum

logger = getLogger(__name__)


class GetDataEngineCsgt:
    timeout: Final[int] = config.request_timeout
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self, plate: PlateInfoDTO) -> None:
        self.plate: PlateInfoDTO = plate
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

    async def get_data(
        self,
    ) -> PlateInfoModel | None: ...

    # TODO: try catch at this
