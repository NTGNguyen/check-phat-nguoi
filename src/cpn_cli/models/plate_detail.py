from typing import Any, override

from pydantic import BaseModel, Field

from cpn_core.models import PlateInfo, ViolationDetail


class PlateDetail(BaseModel):
    plate_info: PlateInfo
    violations: tuple[ViolationDetail, ...] | None = Field(
        description="Danh sách các vi phạm của 1 biển xe",
    )

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
