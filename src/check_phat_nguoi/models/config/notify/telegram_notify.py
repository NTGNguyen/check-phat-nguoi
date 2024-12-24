from check_phat_nguoi.models.config.notify.base_notify import BaseNotifyModel
from check_phat_nguoi.models.config.notify.telegram import TelegramModel


class TelegramNotifyModel(BaseNotifyModel):
    telegram: TelegramModel


__all__ = ["TelegramNotifyModel"]
