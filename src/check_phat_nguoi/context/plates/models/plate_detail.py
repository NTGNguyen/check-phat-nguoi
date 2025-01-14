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

    def __str__(self):
        def create_violation_str(violation: ViolationDetail, index: int) -> str:
            resolution_offices: str | None = (
                f"""
                   Nơi giải quyết vụ việc:
                   {
                    "\n".join(
                        resolution_office_detail
                        for resolution_office_detail in violation.resolution_offices_details
                    )
                }
                """
                if violation.resolution_offices_details
                else None
            )
            # TODO: Keep going on
            violation_str: str = (
                f"Lỗi vi phạm thứ {index}:" + f"\nMàu biển: {violation.color}"
                if violation.color
                else ""
            )
            # violation_str = "\n".join(
            #     line
            #     for line in f"""
            # Lỗi vi phạm thứ {index}:
            #     Màu biển: {violation.color if violation.color else " "}
            #     Thời điểm vi phạm: {violation.date if violation.date else " "}
            #     Vị trí vi phạm: {violation.location if violation.location else " "}
            #     Hành vi vi phạm: {violation.violation if violation.violation else " "}
            #                     Trạng thái: {"Đã xử phạt" if violation.status else ("Chưa xử phạt" if not violation.status else " ")}
            #     Đơn vị phát hiện vi phạm: {violation.enforcement_unit if violation.enforcement_unit else " "}
            # """.splitlines()
            #     if line.strip()
            # )
            return (
                "\n".join([violation_str, resolution_offices])
                if resolution_offices
                else violation_str
            )

        # TODO: Ye going on hehehe
        plate_detail: str = "\n".join(
            line
            for line in f"""
        Biển số: {self.plate}
        Chủ sở hữu: {self.owner if self.owner else " "}
        """.splitlines()
            if line.strip()
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
