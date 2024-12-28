from typing import LiteralString

CONFIG_PATHS: list[LiteralString] = [
    "config.json",
    "check-phat-nguoi.config.json",
    "~/check-phat-nguoi.config.json",
]
SIMPLE_LOG_MESSAGE: LiteralString = "[%(levelname)s]: %(message)s"
DETAIL_LOG_MESSAGE: LiteralString = (
    "%(asctime)s [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"
)

# API from checkphatnguoi.vn
GET_DATA_API_URL_CHECKPHATNGUOI: LiteralString = (
    "https://api.checkphatnguoi.vn/phatnguoi"
)
SEND_MESSAGE_API_URL_TELEGRAM: LiteralString = (
    "https://api.telegram.org/bot{bot_token}/sendMessage"
)
DATETIME_FORMAT_CHECKPHATNGUOI: LiteralString = "%H:%M, %d/%m/%Y"

OFFICE_NAME_PATTERN = r"^\d+\."

MESSAGE_MARKDOWN_PATTERN: LiteralString = """
*🚗 **Thông tin phương tiện**:*
- **Biển kiểm soát:** `{plate}`
- **Chủ sở hữu:** `{owner}'

*⚠️ **Thông tin vi phạm**:*
- **Hành vi vi phạm:** `{action}`
- **Trạng thái:** {status}
- **Thời gian vi phạm:** `{date}`
- **Địa điểm vi phạm** {location}

*🏢 **Đơn vị phát hiện vi phạm**:*
- **{enforcement_unit}**

*📍 **Nơi giải quyết vụ việc**:*
{resolution_locations}
"""

RESOLUTION_LOCATION_MARKDOWN_PATTERN: LiteralString = """
{idx}. **{location_name}
- **Địa chỉ:** {address}
- **Số điện thoại liên lạc:** {phone}

"""
