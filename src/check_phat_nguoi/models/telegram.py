from pydantic import BaseModel


class Telegram(BaseModel):
    bot_token: str
    chat_id: str
