from typing import LiteralString

# API from checkphatnguoi.vn
GET_DATA_API_URL_CHECKPHATNGUOI: LiteralString = (
    "https://api.checkphatnguoi.vn/phatnguoi"
)
API_URL_CSGT_CAPTCHA: LiteralString = (
    "https://www.csgt.vn/lib/captcha/captcha.class.php"
)
API_URL_CSGT_QUERY: LiteralString = (
    "https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax"
)

DATETIME_FORMAT_CHECKPHATNGUOI: LiteralString = "%H:%M, %d/%m/%Y"

OFFICE_NAME_PATTERN: LiteralString = r"^\d+\."
