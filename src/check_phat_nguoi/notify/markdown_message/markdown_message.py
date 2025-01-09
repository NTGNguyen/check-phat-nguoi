from __future__ import annotations

from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.constants import (
    MESSAGE_MARKDOWN_PATTERN,
    RESOLUTION_LOCATION_MARKDOWN_PATTERN,
)
from check_phat_nguoi.context import (
    PlateDetail,
    ResolutionOffice,
)

from .models import MarkdownMessageDetail


class MarkdownMessage:
    def __init__(self, plate_detail: PlateDetail) -> None:
        self.plate_detail: PlateDetail = plate_detail

    @staticmethod
    def _format_location(
        locations_info: tuple[ResolutionOffice, ...] | None,
    ) -> str:
        if locations_info is None:
            return ""
        resolution_markdown: str = ""
        for idx, location_detail in enumerate(locations_info, start=1):
            resolution: str = RESOLUTION_LOCATION_MARKDOWN_PATTERN.substitute(
                idx=idx,
                location_name=location_detail.location_name,
                address=location_detail.address
                if location_detail.address
                else "Không có",
                phone=location_detail.phone if location_detail.phone else "Không có",
            )
            resolution_markdown += resolution + "\n"
        return resolution_markdown

    def _format_message(self) -> tuple[str, ...]:
        return tuple(
            [
                MESSAGE_MARKDOWN_PATTERN.substitute(
                    plate=self.plate_detail.plate,
                    owner="Không"
                    if not self.plate_detail.owner
                    else self.plate_detail.owner,
                    action=vio.action,
                    status="Đã xử phạt" if vio.status else "Chưa xử phạt",
                    date=f"{vio.date}",
                    location=vio.location,
                    enforcement_unit=vio.enforcement_unit,
                    resolution_locations=self._format_location(vio.resolution_office),
                )
                for vio in self.plate_detail.violation
                if not vio.status or config.unpaid_only
            ]
        )

    def generate_message(self) -> MarkdownMessageDetail:
        return MarkdownMessageDetail(
            plate=self.plate_detail.plate,
            violations=self._format_message(),
        )
