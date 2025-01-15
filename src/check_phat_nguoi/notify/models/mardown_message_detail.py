from pydantic import BaseModel, Field


class MarkdownMessageDetail(BaseModel):
    plate: str = Field(description="Biển số")
    messages: tuple[str, ...] = Field(
        description="List chứa các string chứa các thông tin cụ thể về lỗi vi phạm"
    )
