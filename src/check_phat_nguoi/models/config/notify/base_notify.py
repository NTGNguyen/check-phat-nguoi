from pydantic import BaseModel


class BaseNotifyModel(BaseModel):
    enabled: bool = True


__all__ = ["BaseNotifyModel"]
