from re import match as re_match

from pydantic import ConfigDict, Field, field_validator

from cpn_core.notifications.models.base import BaseNotificationEngineConfig


class TelegramNotificationEngineConfig(BaseNotificationEngineConfig):
    model_config = ConfigDict(
        title="Telegram",
        frozen=True,
    )

    bot_token: str = Field(
        description="Bot token Telegram",
        examples=[
            "2780473231:weiruAShGUUx4oLOMoUhd0GiREXSZcCq-uB",
        ],
    )
    chat_id: str = Field(
        description="Chat ID Telegram",
        examples=[
            "-1001790012349",
        ],
    )
    markdown: bool = Field(
        description="Gửi tin nhắn dạng markdown",
        default=True,
    )

    @field_validator("bot_token", mode="after")
    @classmethod
    def validate_bot_token(cls, _bot_token: str) -> str:
        if not re_match(r"^[0-9]+:.+$", _bot_token):
            raise ValueError("Bot token is not valid")
        return _bot_token

    @field_validator("chat_id", mode="after")
    @classmethod
    def validate_chat_id(cls, _chat_id: str) -> str:
        if not re_match(r"^[+-]?[0-9]+$", _chat_id):
            raise ValueError("Chat ID is not valid")
        return _chat_id


__all__ = ["TelegramNotificationEngineConfig"]
