from check_phat_nguoi.utils.singleton import Singleton

from .dto.config import ConfigDTO


class Config(Singleton, ConfigDTO): ...


__all__ = ["Config"]
