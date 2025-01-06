from string import Template
from typing import LiteralString

SEND_MESSAGE_API_URL_TELEGRAM: LiteralString = (
    "https://api.telegram.org/bot{bot_token}/sendMessage"
)
MESSAGE_MARKDOWN_PATTERN = Template("""
*🚗 **Thông tin phương tiện**:*
- **Biển kiểm soát:** `${plate}`
- **Chủ sở hữu:** `${owner}`

*⚠️ **Thông tin vi phạm**:*
- **Hành vi vi phạm:** `${action}`
- **Trạng thái:** ${status}
- **Thời gian vi phạm:** `${date}`
- **Địa điểm vi phạm:** `${location}`

*🏢 **Đơn vị phát hiện vi phạm**:*
- **`${enforcement_unit}`**

*📍 **Nơi giải quyết vụ việc**:*
${resolution_locations}
""")

RESOLUTION_LOCATION_MARKDOWN_PATTERN = Template("""
${idx}. **${location_name}
- **Địa chỉ:** `${address}`
- **Số điện thoại liên lạc:** `${phone}`

""")
