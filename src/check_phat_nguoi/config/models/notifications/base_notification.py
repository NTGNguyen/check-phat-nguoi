from pydantic import BaseModel, ConfigDict, Field


class BaseNotificationConfig(BaseModel):
    model_config = ConfigDict(
        title="Lớp cơ sở notification bao gồm trường enabled cho các lớp kế thừa",
        frozen=True,
    )

    enabled: bool = Field(
        description="Kích hoạt",
        default=True,
    )


__all__ = ["BaseNotificationConfig"]
