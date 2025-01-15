from __future__ import annotations

from typing import Any, override

from pydantic import BaseModel, Field

from check_phat_nguoi.types import VehicleTypeEnum, get_vehicle_enum

from .violation_detail import ViolationDetail


class PlateDetail(BaseModel):
    plate: str
    owner: str | None
    type: VehicleTypeEnum
    violations: tuple[ViolationDetail, ...] | None = Field(
        description="Danh sách các vi phạm của 1 biển xe",
    )

    @override
    def __hash__(self):
        return (
            hash(self.plate)
            + hash(self.owner)
            + hash(self.type)
            + hash(self.violations)
        )

    @override
    def __eq__(self, other: Any):
        if isinstance(other, PlateDetail):
            return (
                self.plate == other.plate
                and self.owner == other.owner
                and get_vehicle_enum(self.type) == get_vehicle_enum(other.type)
                and (
                    all(x == y for x, y in zip(self.violations, other.violations))
                    if self.violations and other.violations
                    else (not self.violations and not other.violations)
                )
            )
        return False

    # TODO: Handle show details later when main updates that option
    def __str__(self) -> str:
        def create_violation_str(violation: ViolationDetail, index: int) -> str:
            violation_str: str = (
                f"Lỗi vi phạm thứ {index}:"
                + (f"\nMàu biển: {violation.color}" if violation.color else "")
                + (f"\nThời điểm vi phạm: {violation.date}" if violation.date else "")
                + (
                    f"\nVị trí vi phạm: {violation.location}"
                    if violation.location
                    else ""
                )
                + (
                    f"\nHành vi vi phạm: {violation.violation}"
                    if violation.violation
                    else ""
                )
                + (
                    f"\nTrạng thái: {'Chưa xử phạt' if not violation.status else 'Đã xử phạt'}"
                    if violation.status is not None
                    else ""
                )
                + (
                    f"\nĐơn vị phát hiện vi phạm: {violation.enforcement_unit}"
                    if violation.enforcement_unit
                    else ""
                )
            )
            resolution_offices: str | None = (
                "\n"
                + "Nơi giải quyết vụ việc:"
                + "\n"
                + "\n".join(
                    resolution_office_detail.strip()
                    for resolution_office_detail in violation.resolution_offices
                )
                if violation.resolution_offices
                else None
            )
            return violation_str + (resolution_offices if resolution_offices else "")

        plate_detail: str = f"Biển số: {self.plate}" + (
            f"\nChủ sở hữu: {self.owner}" if self.owner else ""
        )

        if self.violations:
            return (
                plate_detail
                + "\n"
                + "\n".join(
                    create_violation_str(violation, index)
                    for index, violation in enumerate(self.violations, start=1)
                )
            )
        return plate_detail


__all__ = ["PlateDetail"]
