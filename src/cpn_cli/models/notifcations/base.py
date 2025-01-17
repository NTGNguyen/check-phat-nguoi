from pydantic import BaseModel, Field


class BaseNotificationConfig(BaseModel):
    enabled: bool = Field(
        description="Kích hoạt",
        default=True,
    )
