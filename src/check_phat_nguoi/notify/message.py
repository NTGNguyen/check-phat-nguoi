from check_phat_nguoi.config.dto.config import ConfigDTO
from check_phat_nguoi.context import PlateInfoModel, PlatesModel
from check_phat_nguoi.context.plate_context.models.resolution_office import (
    ResolutionOfficeModel,
)

from ..modules.constants.notify import (
    MESSAGE_MARKDOWN_PATTERN,
    RESOLUTION_LOCATION_MARKDOWN_PATTERN,
)


class Message:
    def __init__(self, plate_context_object: PlatesModel, config_object: ConfigDTO):
        self._plate_context_object: PlatesModel = plate_context_object
        self._config_object: ConfigDTO = config_object

    @staticmethod
    def format_location(
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

    @staticmethod
    def format_message(
        plate_info_context: PlateInfoModel, unpaid_paid_only: bool
    ) -> tuple[str, ...]:
        return tuple(
            [
                MESSAGE_MARKDOWN_PATTERN.substitute(
                    plate=plate_info_context.plate,
                    owner="Không biết"
                    if not plate_info_context.owner
                    else plate_info_context.owner,
                    action=vio.action,
                    status="Đã nộp phạt" if vio.status else "Chưa nộp phạt",
                    date=f"{vio.date}",
                    location=vio.location,
                    enforcement_unit=vio.enforcement_unit,
                    resolution_locations=Message.format_location(vio.resolution_office),
                )
                for vio in plate_info_context.violation
                if not vio.status or unpaid_paid_only
            ]
        )

    def format_messages(self) -> dict[str, tuple[str, ...]]:
        message_dict: dict[str, tuple[str, ...]] = {}
        for plate_info_context in self._plate_context_object.plates:
            message_dict[plate_info_context.plate] = Message.format_message(
                plate_info_context, self._config_object.unpaid_only
            )
        return message_dict
