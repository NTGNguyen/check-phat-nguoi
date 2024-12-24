from pydantic import BaseModel


class BaseNotifyConfigModel(BaseModel):
    enabled: bool = True


__all__ = ["BaseNotifyConfigModel"]
