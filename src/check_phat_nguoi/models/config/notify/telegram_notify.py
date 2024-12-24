from check_phat_nguoi.models.config.notify.base_notify import BaseNotify
from check_phat_nguoi.models.config.notify.telegram import Telegram


class TelegramNotify(BaseNotify):
    telegram: Telegram


__all__ = ["TelegramNotify"]
