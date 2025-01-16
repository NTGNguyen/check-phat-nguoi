from string import Template
from typing import Final

from cpn_core.models import MessageDetail, ViolationDetail
from cpn_core.models.plate_info import PlateInfo

# FIXME: Migrate later @NTGNguyen
MESSAGE_MARKDOWN_PATTERN: Final[Template] = Template("""
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

RESOLUTION_LOCATION_MARKDOWN_PATTERN: Final[Template] = Template("""
${idx}. **${location_name}
- **Địa chỉ:** `${address}`
- **Số điện thoại liên lạc:** `${phone}`

""")


class MarkdownMessage:
    def __init__(
        self,
        plate_info: PlateInfo,
        violations: tuple[ViolationDetail, ...],
        *,
        pending_fines_only: bool = True,
    ) -> None:
        self._plate_info: PlateInfo = plate_info
        self._violations: tuple[ViolationDetail, ...] = violations
        self._pending_fines_only: bool = pending_fines_only

    def _format_message(self) -> tuple[str, ...]:
        if not self._violations:
            return ()
        return tuple(
            [
                MESSAGE_MARKDOWN_PATTERN.substitute(
                    plate=self._plate_info.plate,
                    owner="Không"
                    if not self._plate_info.owner
                    else self._plate_info.owner,
                    action=violation.violation,
                    status="Đã xử phạt" if violation.status else "Chưa xử phạt",
                    date=f"{violation.date}",
                    location=violation.location,
                    enforcement_unit=violation.enforcement_unit,
                    # FIXME: The name of arg doesn't change when refactoring name. Maybe find another way, not format string like this. Maybe, if check string
                    resolution_locations="\n".join(violation.resolution_offices)
                    if violation.resolution_offices
                    else "",
                )
                for violation in self._violations
                if not violation.status or not self._pending_fines_only
            ]
        )

    def generate_message(self) -> MessageDetail:
        return MessageDetail(
            plate=self._plate_info.plate,
            messages=self._format_message(),
        )
