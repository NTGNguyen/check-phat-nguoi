from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MessageDetail:
    plate: str
    messages: tuple[str, ...]
    time: datetime = field(default_factory=datetime.now)
