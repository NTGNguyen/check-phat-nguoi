from __future__ import annotations

from pydantic import BaseModel, Field


class ResolutionOffice(BaseModel):
    location_name: str = Field(description="Nơi giải quyết vụ việc")
    address: str | None = Field(description="Địa chỉ", default=None)
    phone: str | None = Field(description="Số điện thoại", default=None)
