from logging import getLogger
from threading import Thread
from typing import LiteralString

import requests

from check_phat_nguoi.models.notify.telegram_notify import TelegramNotifyModel
from check_phat_nguoi.utils.constants import SEND_MESSAGE_API_URL_TELEGRAM as API_URL

logger = getLogger(__name__)


class Telegram:
    def __init__(
        self,
        telegram_notify_object: TelegramNotifyModel,
        message_dict: dict[str, LiteralString],
    ):
        self._telegram_notify_object: TelegramNotifyModel = telegram_notify_object
        self._message_dict: dict[str, LiteralString] = message_dict

    def _send_message(self, message: LiteralString, timeout=10) -> None:
        url = API_URL.format(bot_token=self._telegram_notify_object.telegram.bot_token)
        payload = {
            "chat_id": self._telegram_notify_object.telegram.chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Request successful: {response.status_code}")
        except requests.exceptions.ConnectionError:
            logger.error(f"Unable to connect to {url}")
        except requests.exceptions.Timeout:
            logger.error(f"Time out of {timeout} seconds from URL {url}")

    def mutithread_send_message(self) -> None:
        threads: list[Thread] = []
        for _, message in self._message_dict.items():
            thread = Thread(target=self._send_message, args=(message))
            threads.append(thread)
            thread.start()
        for idx, thread in enumerate(threads, start=1):
            try:
                thread.join()
            except Exception:
                logger.error(
                    f"An error occurs while sending message in thread number {idx}"
                )
