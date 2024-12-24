from pydantic import BaseModel


class PlateInfoConfigModel(BaseModel):
    plate: str
    owner: str | None = None


__all__ = ["PlateInfoConfigModel"]
