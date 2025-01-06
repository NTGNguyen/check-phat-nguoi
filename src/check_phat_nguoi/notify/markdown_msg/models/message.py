from pydantic import BaseModel, Field


class MessagesModel(BaseModel):
    plate: str = Field(description="Biển số")
    vio_msgs: tuple[str, ...] = Field(
        description="List chứa các string chứa các thông tin cụ thể về lỗi vi phạm sau"
    )
