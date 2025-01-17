from datetime import datetime
from typing import override

from pydantic import BaseModel

from cpn_core.types.vehicle_type import VehicleTypeEnum, get_vehicle_str_vie


class ViolationDetail(BaseModel):
    plate: str | None
    color: str | None
    type: VehicleTypeEnum | None
    date: datetime | None
    location: str | None
    violation: str | None
    status: bool | None
    enforcement_unit: str | None
    resolution_offices: tuple[str, ...] | None

    def get_str(self, *, show_less_detail: bool, markdown: bool) -> str:
        if markdown:
            return self._get_markdown_message(show_less_detail)
        else:
            return self._get_raw_messages(show_less_detail)

    def _get_raw_messages(self, show_less_detail: bool) -> str:
        message: str
        if show_less_detail:
            message = (
                (f"\nThời điểm: {self.date}" if self.date else "")
                + (f"\nVị trí: {self.location}" if self.location else "")
                + (f"\nHành vi: {self.violation}" if self.violation else "")
                + (
                    f"\nTrạng thái: {'Đã xử phạt' if self.status else 'Chưa xử phạt'}"
                    if self.status
                    else ""
                )
                + (
                    f"\nĐơn vị phát hiện: {self.enforcement_unit}"
                    if self.enforcement_unit
                    else ""
                )
                + (
                    (
                        "\n"
                        + "\n".join(
                            f"- {resolution_office}"
                            for resolution_office in self.resolution_offices
                        )
                    )
                    if self.resolution_offices
                    else ""
                )
            ).strip()
        else:
            message = (
                (f"Biển: {self.plate}" if self.plate else "")
                + (f"\nMàu biển: {self.color}" if self.color else "")
                + (f"\nLoại xe: {get_vehicle_str_vie(self.type)}" if self.type else "")
                + (f"\nThời điểm: {self.date}" if self.date else "")
                + (f"\nVị trí: {self.location}" if self.location else "")
                + (f"\nHành vi: {self.violation}" if self.violation else "")
                + (
                    f"\nTrạng thái: {'Đã xử phạt' if self.status else 'Chưa xử phạt'}"
                    if self.status
                    else ""
                )
                + (
                    f"\nĐơn vị phát hiện: {self.enforcement_unit}"
                    if self.enforcement_unit
                    else ""
                )
                + (
                    (
                        "\n"
                        + "\n".join(
                            f"- {resolution_office}"
                            for resolution_office in self.resolution_offices
                        )
                    )
                    if self.resolution_offices
                    else ""
                )
            ).strip()
        return "Thông tin vi phạm:\n" + message

    def _get_markdown_message(self, show_less_detail: bool) -> str:
        message: str
        if show_less_detail:
            message = (
                (f"\n*Thời điểm:* {self.date}" if self.date else "")
                + (f"\n*Vị trí:* {self.location}" if self.location else "")
                + (f"\n*Hành vi:* {self.violation}" if self.violation else "")
                + (
                    f"\n*Trạng thái:* {'Đã xử phạt ✅' if self.status else 'Chưa xử phạt ❌'}"
                    if self.status
                    else ""
                )
                + (
                    f"\n*Đơn vị phát hiện:* {self.enforcement_unit}"
                    if self.enforcement_unit
                    else ""
                )
                + (
                    (
                        "\n"
                        + "\n".join(
                            f"- {resolution_office}"
                            for resolution_office in self.resolution_offices
                        )
                    )
                    if self.resolution_offices
                    else ""
                )
            ).strip()
        else:
            message = (
                (f"*Biển:* {self.plate}" if self.plate else "")
                + (f"\n*Màu biển:* {self.color}" if self.color else "")
                + (
                    f"\n*Loại xe:* {get_vehicle_str_vie(self.type)}"
                    if self.type
                    else ""
                )
                + (f"\n*Thời điểm:* {self.date}" if self.date else "")
                + (f"\n*Vị trí:* {self.location}" if self.location else "")
                + (f"\n*Hành vi:* {self.violation}" if self.violation else "")
                + (
                    f"\n*Trạng thái:* {'Đã xử phạt ✅' if self.status else 'Chưa xử phạt ❌'}"
                    if self.status
                    else ""
                )
                + (
                    f"\n*Đơn vị phát hiện:* {self.enforcement_unit}"
                    if self.enforcement_unit
                    else ""
                )
                + (
                    (
                        "\n"
                        + "\n".join(
                            f"- {resolution_office}"
                            for resolution_office in self.resolution_offices
                        )
                    )
                    if self.resolution_offices
                    else ""
                )
            ).strip()
        return "*⚠️ Thông tin vi phạm:*\n" + message

    @override
    def __hash__(self):
        return (
            hash(self.plate) + hash(self.color) + hash(self.date) + hash(self.location)
        )
