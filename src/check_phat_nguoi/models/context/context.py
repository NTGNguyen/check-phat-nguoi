from pydantic import BaseModel

from check_phat_nguoi.models.context.plate_info import PlateInfo


class Context(BaseModel):
    data: list[PlateInfo] = []


__all__ = ["Context"]
