from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseNotificationEngineConfig(BaseModel):
    model_config = ConfigDict(
        title="Lớp cơ sở notification engine",
        alias_generator=to_camel,
    )


__all__ = ["BaseNotificationEngineConfig"]
