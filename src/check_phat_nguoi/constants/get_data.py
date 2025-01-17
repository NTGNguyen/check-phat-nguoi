from typing import LiteralString

# API from checkphatnguoi.vn
GET_DATA_API_URL_CHECKPHATNGUOI: LiteralString = (
    "https://api.checkphatnguoi.vn/phatnguoi"
)
API_URL_PHATNGUOI: LiteralString = "https://api.phatnguoi.vn/web/tra-cuu"
API_URL_CSGT_CAPTCHA: LiteralString = (
    "https://www.csgt.vn/lib/captcha/captcha.class.php"
)
API_URL_CSGT_QUERY_1: LiteralString = (
    "https://www.csgt.vn/?mod=contact&task=tracuu_post&ajax"
)
API_URL_CSGT_QUERY_2: LiteralString = "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html?&LoaiXe={vehicle_type}&BienKiemSoat={plate}"
API_URL_ETRAFFIC: LiteralString = "https://api.zm.io.vn/v1/csgt/tracuu"
DATETIME_FORMAT_CHECKPHATNGUOI: LiteralString = "%H:%M, %d/%m/%Y"

OFFICE_NAME_PATTERN: LiteralString = r"^\d+\."
