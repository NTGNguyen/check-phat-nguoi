from re import match as re_match

from pydantic import ConfigDict, Field, field_validator

from .base_engine import BaseNotificationEngineConfig


class DiscordNotificationEngineConfig(BaseNotificationEngineConfig):
    config_model: ConfigDict = ConfigDict(title="Discord", frozen=True)
    bot_token: str = Field(
        description="bot token in discord",
        examples=[
            "MTMzNzg4Ujq0NDI0NDYgNTcyMA.GpITQg.beoF9OxJScbKJwEz5Udy6bzrQJ8zI4BvndbaBA"
        ],
    )
    user_id: int = Field(
        description="User id in discord",
        examples=[
            834242026182672436,
        ],
    )

    @field_validator("bot_token", mode="after")
    @classmethod
    def validate_bot_token(cls, _bot_token: str) -> str:
        if not re_match(
            r"^[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+$", _bot_token
        ):
            raise ValueError("Bot token is not valid")
        return _bot_token

    @field_validator("user_id", mode="after")
    @classmethod
    def validate_user_id(cls, _user_id: int) -> int:
        if not re_match(r"^\d{18,19}$", f"{_user_id}"):
            raise ValueError("User id is not valid")
        return _user_id


__all__ = ["DiscordNotificationEngineConfig"]
