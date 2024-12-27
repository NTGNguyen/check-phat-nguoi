from .base_notify import BaseNotifyDTO
from .telegram import TelegramDTO


class TelegramNotifyDTO(BaseNotifyDTO):
    telegram: TelegramDTO


__all__ = ["TelegramNotifyDTO"]
