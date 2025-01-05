from pydantic import BaseModel, Field

from check_phat_nguoi.config import config
from check_phat_nguoi.context import (
    PlateInfoModel,
    ResolutionOfficeModel,
    plates_context,
)

from ..constants.notify import (
    MESSAGE_MARKDOWN_PATTERN,
    RESOLUTION_LOCATION_MARKDOWN_PATTERN,
)


class MessagesModel(BaseModel):
    plate: str = Field(description="Biển số")
    messages: tuple[str, ...] = Field(
        description="List chứa các string chứa các thông tin cụ thể về lỗi vi phạm sau"
    )


# FIXME: Nếu không cần instance member nào thì bỏ class, chỉ dùng function để lấy message
class Message:
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

    @staticmethod
    def _format_message(
        plate_info_context: PlateInfoModel, unpaid_only: bool
    ) -> tuple[str, ...]:
        return tuple(
            [
                MESSAGE_MARKDOWN_PATTERN.substitute(
                    plate=plate_info_context.plate,
                    owner="Không"
                    if not plate_info_context.owner
                    else plate_info_context.owner,
                    action=vio.action,
                    status="Đã xử phạt" if vio.status else "Chưa xử phạt",
                    date=f"{vio.date}",
                    location=vio.location,
                    enforcement_unit=vio.enforcement_unit,
                    resolution_locations=Message._format_location(
                        vio.resolution_office
                    ),
                )
                for vio in plate_info_context.violation
                if not vio.status or unpaid_only
            ]
        )

    @staticmethod
    def format_messages() -> tuple[MessagesModel, ...]:
        return tuple(
            [
                MessagesModel(
                    plate=plate_info_context.plate,
                    messages=Message._format_message(
                        plate_info_context, unpaid_only=config.unpaid_only
                    ),
                )
                for plate_info_context in plates_context.plates
            ]
        )
