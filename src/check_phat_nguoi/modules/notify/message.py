from typing import Dict, LiteralString

from check_phat_nguoi.context import PlateInfoModel, PlatesModel
from check_phat_nguoi.context.plate_context.models.resolution_office import (
    ResolutionOfficeModel,
)
from check_phat_nguoi.utils.constants import (
    MESSAGE_MARKDOWN_PATTERN,
    RESOLUTION_LOCATION_MARKDOWN_PATTERN,
)


class Message:
    def __init__(self, plate_context_object: PlatesModel):
        self._plate_context_object: PlatesModel = plate_context_object

    @staticmethod
    def format_location(
        locations_info: tuple[ResolutionOfficeModel, ...] | None,
    ) -> str:
        if locations_info is None:
            return ""
        resolution_markdown: str = ""
        for idx, location_detail in enumerate(locations_info, start=1):
            resolution: str = RESOLUTION_LOCATION_MARKDOWN_PATTERN.format(
                idx=idx,
                location_name=location_detail.location_name,
                address=location_detail.address
                if location_detail.address
                else "Không có",
                phone=location_detail.phone if location_detail.phone else "Không có",
            )
            resolution_markdown += resolution + "\n"
        return resolution_markdown

    @staticmethod
    def format_message(
        plate_info_context: PlateInfoModel,
    ) -> tuple[str, ...]:
        return tuple(
            MESSAGE_MARKDOWN_PATTERN.format(
                plate=plate_info_context.plate,
                owner=plate_info_context.owner,
                action=vio.action,
                status=vio.status,
                date=f"{vio.date}",
                location=vio.enforcement_unit,
                resolution_locations=Message.format_location(vio.resolution_office),
            )
            for vio in plate_info_context.violation
            if vio.status
        )

    def format_messages(self) -> dict[str, tuple[str, ...]]:
        message_dict: dict[str, tuple[str, ...]] = {}
        for plate_info_context in self._plate_context_object.plates:
            message_dict[plate_info_context.plate] = Message.format_message(
                plate_info_context
            )
        return message_dict
