from pydantic import BaseModel, ConfigDict


class BaseNotificationEngineConfig(BaseModel):
    model_config = ConfigDict(
        title="Lớp cơ sở notification engine",
        frozen=True,
    )


__all__ = ["BaseNotificationEngineConfig"]
