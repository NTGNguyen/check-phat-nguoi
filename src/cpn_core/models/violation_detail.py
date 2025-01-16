from dataclasses import dataclass
from datetime import datetime
from typing import override

from cpn_core.types import VehicleTypeEnum, get_vehicle_str_vie


@dataclass(frozen=True, slots=True)
class ViolationDetail:
    plate: str
    color: str
    type: VehicleTypeEnum
    date: datetime
    location: str
    violation: str
    status: bool
    enforcement_unit: str
    resolution_offices: tuple[str, ...]

    @override
    def __str__(self) -> str:
        return (
            (f"Biển vi phạm: {self.plate}" if self.plate else "")
            + (f"\nMàu biển: {self.color}" if self.color else "")
            + (f"\nLoại xe: {get_vehicle_str_vie(self.type)}" if self.type else "")
            + (f"\nThời điểm vi phạm: {self.date}" if self.date else "")
            + (f"\nVị trí vi phạm: {self.location}" if self.location else "")
            + (f"\nHành vi vi phạm: {self.violation}" if self.violation else "")
            + (
                f"\nTrạng thái: {'Đã xử phạt' if self.status else 'Chưa xử phạt'}"
                if self.status
                else ""
            )
            + (
                f"\nĐơn vị phát hiện vi phạm: {self.enforcement_unit}"
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

    @override
    def __hash__(self):
        return (
            hash(self.plate) + hash(self.color) + hash(self.date) + hash(self.location)
        )
