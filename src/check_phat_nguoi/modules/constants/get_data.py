from typing import LiteralString

# API from checkphatnguoi.vn
GET_DATA_API_URL_CHECKPHATNGUOI: LiteralString = (
    "https://api.checkphatnguoi.vn/phatnguoi"
)
SEND_MESSAGE_API_URL_TELEGRAM: LiteralString = (
    "https://api.telegram.org/bot{bot_token}/sendMessage"
)
DATETIME_FORMAT_CHECKPHATNGUOI: LiteralString = "%H:%M, %d/%m/%Y"

OFFICE_NAME_PATTERN = r"^\d+\."
