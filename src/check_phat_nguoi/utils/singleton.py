from typing import Self


class Singleton:
    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


__all__ = ["Singleton"]
