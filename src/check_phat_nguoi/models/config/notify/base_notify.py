from pydantic import BaseModel


class BaseNotify(BaseModel):
    enabled: bool = True


__all__ = ["BaseNotify"]
