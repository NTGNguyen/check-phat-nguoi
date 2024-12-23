from pydantic import BaseModel

from check_phat_nguoi.models.plate_info import PlateInfo
from check_phat_nguoi.models.telegram import Telegram


class Config(BaseModel):
    data: list[PlateInfo] = []
    notify: list[Telegram] = []
