import re
from datetime import datetime
from typing import Dict, Literal

from pydantic import BaseModel, Field, field_validator

from check_phat_nguoi.utils.constants import OFFICE_NAME_PATTERN


class ViolationModel(BaseModel):
    type: Literal["Ô tô", "Xe máy", "Xe đạp điện"] | None = Field(
        description="Loại phương tiện giao thông", default=None
    )
    date: datetime | None = Field(description="Thời điểm vi phạm", default=None)
    location: str | None = Field(description="Vị trí vi phạm", default=None)
    action: str | None = Field(description="Hành vi vi phạm", default=None)
    status: bool | None = Field(
        description="Đã nộp phạt (True) / Chưa nộp phạt (False)", default=None
    )
    enforcement_unit: str | None = Field(
        description="Đơn vị phát hiện vi phạm", default=None
    )
    resolution_office: Dict[str, Dict] | None = Field(
        description="Nơi giải quyết vụ việc", default=None
    )

    @field_validator("resolution_office", mode="before")
    def parse_resolution_office(values) -> Dict[str, Dict]:
        offices_list: list[str] = values["raw_data"]
        parsed_office_dict: Dict[str, Dict] = []
        current_name = None

        for office_info in offices_list:
            if re.match(OFFICE_NAME_PATTERN, office_info):
                current_name = office_info.split(".", 1)[1].strip()
                parsed_office_dict[current_name] = {"Address": None, "Phone": None}
            elif "Địa chỉ" in office_info:
                if current_name:
                    parsed_office_dict[current_name]["Address"] = office_info.split(
                        ":", 1
                    )[1].strip()
            elif "Số điện thoại" in office_info:
                if current_name:
                    parsed_office_dict[current_name]["Phone"] = office_info.split(
                        ":", 1
                    )[1].strip()

        return parsed_office_dict
