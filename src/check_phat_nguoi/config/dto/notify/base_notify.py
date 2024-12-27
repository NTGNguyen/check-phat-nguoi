from pydantic import BaseModel, Field


class BaseNotifyDTO(BaseModel):
    enabled: bool = Field(description="Kích hoạt", default=True)


__all__ = ["BaseNotifyDTO"]
