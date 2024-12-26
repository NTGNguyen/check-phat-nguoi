from pydantic import BaseModel, Field


class BaseNotifyConfigModel(BaseModel):
    enabled: bool = Field(description="Kích hoạt", default=True)


__all__ = ["BaseNotifyConfigModel"]
