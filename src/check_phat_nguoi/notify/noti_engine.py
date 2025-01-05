from abc import abstractmethod


class NotificationEngine:
    # FIXME: Lấy timeout từ config gắn vào class mem (không phải instance mem)
    @abstractmethod
    async def send_messages(self) -> None: ...
