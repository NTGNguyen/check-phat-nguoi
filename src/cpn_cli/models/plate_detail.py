from typing import Any, override

from pydantic import BaseModel, Field, computed_field

from cpn_core.models.plate_info import PlateInfo
from cpn_core.models.violation_detail import ViolationDetail


class PlateDetail(BaseModel):
    plate_info: PlateInfo = Field(
        description="Thông tin biển số phương tiện",
    )
    violations: tuple[ViolationDetail, ...] | None = Field(
        description="Danh sách các vi phạm của 1 biển xe",
    )

    @computed_field
    @property
    def total_fines(self) -> int | None:
        if not self.violations:
            return
        return len(self.violations)

    @computed_field
    @property
    def total_peding_fines(self) -> int | None:
        if not self.violations:
            return None
        return len(
            tuple(violation for violation in self.violations if not violation.status)
        )

    def get_strs(self, *, show_less_detail: bool, markdown: bool) -> tuple[str, ...]:
        if not self.violations:
            return ()
        plate_info: str = self.plate_info.get_str(
            show_less_detail=show_less_detail, markdown=markdown
        )
        violations: tuple[str, ...] = tuple(
            violation.get_str(show_less_detail=show_less_detail, markdown=markdown)
            for violation in self.violations
        )
        return tuple(f"{plate_info}\n{violation}" for violation in violations)

    @override
    def __hash__(self):
        return hash(self.plate_info) + hash(self.violations)

    @override
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PlateDetail):
            return self.plate_info == other.plate_info and (
                all(x == y for x, y in zip(self.violations, other.violations))
                if self.violations and other.violations
                else (not self.violations and not other.violations)
            )
        return False

    # TODO: Handle show details later when main updates that option
    @override
    def __str__(self) -> str:
        return (
            (
                f"{self.plate_info}\n\n"
                + "\n".join(
                    f"Lỗi vi phạm #{order}:\n{violation}\n"
                    for order, violation in enumerate(self.violations, start=1)
                )
            )
            if self.violations
            else str(self.plate_info)
        ).strip()


__all__ = ["PlateDetail"]
