from re import match as re_match

from pydantic import BaseModel, field_validator


class TelegramConfigModel(BaseModel):
    bot_token: str
    chat_id: str

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
            raise ValueError("Bot token is not valid")
        return _chat_id


__all__ = ["TelegramConfigModel"]
