from abc import abstractmethod


class NotificationEngine:
    @abstractmethod
    async def send_messages(self) -> None: ...
