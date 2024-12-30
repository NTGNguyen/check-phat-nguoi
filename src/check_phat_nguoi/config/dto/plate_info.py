from pydantic import BaseModel, Field


class PlateInfoDTO(BaseModel):
    plate: str = Field(
        description="Biển số",
        title="Biển số",
        examples=["60A64685", "98-A-56604", "30-F88251", "59XB-00000"],
    )
    owner: str | None = Field(
        description="Ghi chú chủ sở hữu (phù hợp khi dùng notify ai đó)",
        title="Ghi chú chủ sở hữu",
        examples=["@kevinnitro", "dad"],
        default=None,
    )

    def __hash__(self):
        return hash(self.plate)

    def __eq__(self, other):
        if isinstance(other, PlateInfoDTO):
            return self.plate == other.plate
        return False


__all__ = ["PlateInfoDTO"]
