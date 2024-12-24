from pydantic import BaseModel

from check_phat_nguoi.models.config.notify.telegram import Telegram


class TelegramNotify(BaseModel):
    telegram: Telegram


__all__ = ["TelegramNotify"]
