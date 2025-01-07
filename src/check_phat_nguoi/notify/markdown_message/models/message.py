from pydantic import BaseModel, Field


class MessagesModel(BaseModel):
    plate: str = Field(description="Biển số")
    violations: tuple[str, ...] = Field(
        description="List chứa các string chứa các thông tin cụ thể về lỗi vi phạm sau"
    )
