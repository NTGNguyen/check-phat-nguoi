from pydantic import BaseModel


class PlateInfoModel(BaseModel):
    plate: str
    owner: str | None = None


__all__ = ["PlateInfoModel"]
