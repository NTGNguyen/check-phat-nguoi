from check_phat_nguoi.models.notify.base_notify import BaseNotifyConfigModel
from check_phat_nguoi.models.notify.telegram import TelegramConfigModel


class TelegramNotifyModel(BaseNotifyConfigModel):
    telegram: TelegramConfigModel


__all__ = ["TelegramNotifyModel"]
