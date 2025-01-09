from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseNotificationConfig(BaseModel):
    model_config = ConfigDict(
        title="Lớp cơ sở notification bao gồm trường enabled cho các lớp kế thừa",
        alias_generator=to_camel,
    )

    enabled: bool = Field(
        description="Kích hoạt",
        default=True,
        frozen=True,
    )


__all__ = ["BaseNotificationConfig"]
