from __future__ import annotations

from check_phat_nguoi.config_reader import config
from check_phat_nguoi.constants import MESSAGE_MARKDOWN_PATTERN
from check_phat_nguoi.context import PlateDetail

from .models import MarkdownMessageDetail


class MarkdownMessage:
    def __init__(self, plate_detail: PlateDetail) -> None:
        self._plate_detail: PlateDetail = plate_detail

    def _format_message(self) -> tuple[str, ...]:
        if not self._plate_detail.violations:
            return ()
        return tuple(
            [
                MESSAGE_MARKDOWN_PATTERN.substitute(
                    plate=self._plate_detail.plate,
                    owner="Không"
                    if not self._plate_detail.owner
                    else self._plate_detail.owner,
                    action=vio.violation,
                    status="Đã xử phạt" if vio.status else "Chưa xử phạt",
                    date=f"{vio.date}",
                    location=vio.location,
                    enforcement_unit=vio.enforcement_unit,
                    # FIXME: The name of arg doesn't change when refactoring name. Maybe find another way, not format string like this. Maybe, if check string
                    resolution_locations="\n".join(vio.resolution_offices)
                    if vio.resolution_offices
                    else "",
                )
                for vio in self._plate_detail.violations
                if not vio.status or not config.pending_fines_only
            ]
        )

    def generate_message(self) -> MarkdownMessageDetail:
        return MarkdownMessageDetail(
            plate=self._plate_detail.plate,
            messages=self._format_message(),
        )
