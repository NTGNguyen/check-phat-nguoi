from pydantic import BaseModel


class PlateInfo(BaseModel):
    plate: str
    owner: str | None = None

    # NOTE: Dô đây lấy regex match check nha Ngẽn
    r"""
    if not re_match(r"^[0-9]{2}-?\w{1,2}-?\d{4,5}$", _plate):
        logger.warning(f"plate {_plate} may not be valid")
    """


__all__ = ["PlateInfo"]
