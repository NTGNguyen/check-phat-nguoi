from __future__ import annotations

from check_phat_nguoi.config.config_reader import config
from check_phat_nguoi.constants import (
    MESSAGE_MARKDOWN_PATTERN,
    RESOLUTION_LOCATION_MARKDOWN_PATTERN,
)
from check_phat_nguoi.context import (
    PlateInfoModel,
    ResolutionOfficeModel,
)

from .models import MessagesModel


class MdMsg:
    def __init__(self, plate_info: PlateInfoModel) -> None:
        self.plate_info: PlateInfoModel = plate_info

    @staticmethod
    def _format_location(
        locations_info: tuple[ResolutionOfficeModel, ...] | None,
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
                    plate=self.plate_info.plate,
                    owner="Không"
                    if not self.plate_info.owner
                    else self.plate_info.owner,
                    action=vio.action,
                    status="Đã xử phạt" if vio.status else "Chưa xử phạt",
                    date=f"{vio.date}",
                    location=vio.location,
                    enforcement_unit=vio.enforcement_unit,
                    resolution_locations=self._format_location(vio.resolution_office),
                )
                for vio in self.plate_info.violation
                if not vio.status or config.unpaid_only
            ]
        )

    def generate_msg(self) -> MessagesModel:
        return MessagesModel(
            plate=self.plate_info.plate,
            vio_msgs=self._format_message(),
        )
