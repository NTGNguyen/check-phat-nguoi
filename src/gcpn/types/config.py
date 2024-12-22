from dataclasses import dataclass


@dataclass(slots=True)
class Config:
    bien_so: str


__all__ = ["Config"]
