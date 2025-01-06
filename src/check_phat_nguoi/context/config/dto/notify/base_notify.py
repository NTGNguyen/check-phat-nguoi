from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseNotifyDTO(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    enabled: bool = Field(
        description="Kích hoạt",
        default=True,
        frozen=True,
    )


__all__ = ["BaseNotifyDTO"]
