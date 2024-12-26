from typing import Dict, LiteralString

from check_phat_nguoi.models.context.plate_context.plate_context import (
    PlatesContextModel,
)
from check_phat_nguoi.models.context.plate_context.plate_info import (
    PlateInfoContextModel,
)
from check_phat_nguoi.utils.constants import (
    DATETIME_FORMAT_CHECKPHATNGUOI,
    MESSAGE_MARKDOWN_PATTERN,
    RESOLUTION_LOCATION_MARKDOWN_PATTERN,
)


class Message:
    def __init__(self, plate_context_object: PlatesContextModel):
        self._plate_context_object: PlatesContextModel = plate_context_object

    @staticmethod
    def format_location(locations_info: Dict) -> LiteralString:
        resolution_markdown: LiteralString = """"""
        for idx, location_name, location_detail in enumerate(
            locations_info.items(), start=1
        ):
            resolution: LiteralString = RESOLUTION_LOCATION_MARKDOWN_PATTERN.format(
                idx=idx,
                location_name=location_name,
                address=location_detail["Address"]
                if location_detail["Address"]
                else "Không có",
                phone=location_detail["Phone"]
                if location_detail["Phone"]
                else "Không có",
            )
            resolution_markdown += resolution + "\n"
        return resolution_markdown

    @staticmethod
    def format_message(
        plate_info_context: PlateInfoContextModel,
    ) -> list[LiteralString]:
        return [
            MESSAGE_MARKDOWN_PATTERN.format(
                plate=plate_info_context.plate,
                owner=plate_info_context.owner,
                action=vio.action,
                status=vio.status,
                date=vio.date.strftime(
                    DATETIME_FORMAT_CHECKPHATNGUOI,
                    location=vio.enforcement_unit,
                    resolution_locations=Message.format_location(vio.resolution_office),
                ),
            )
            for vio in plate_info_context.violation
        ]

    def format_messages(self) -> dict[str, list[LiteralString]]:
        message_dict: dict[str, list[LiteralString]] = {}
        for plate_info_context in self._plate_context_object.plates:
            message_dict[f"{plate_info_context.plate}"] = Message.format_message(
                plate_info_context
            )
        return message_dict
