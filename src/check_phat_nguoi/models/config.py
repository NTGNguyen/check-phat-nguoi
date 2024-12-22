from pydantic import BaseModel

from .plate_info import PlateInfo


class Config(BaseModel):
    data: list[PlateInfo]
