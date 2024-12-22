from pydantic import BaseModel


class PlateInfo(BaseModel):
    plate: str
    owner: str | None = None
