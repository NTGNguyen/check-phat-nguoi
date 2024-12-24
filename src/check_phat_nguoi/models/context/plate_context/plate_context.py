from typing import Dict

from pydantic import BaseModel

from check_phat_nguoi.models.context.plate_context.plate_info import (
    PlateInfoContextModel,
)


class PlatesContextModel(BaseModel):
    plates: list[PlateInfoContextModel] = []

    def get_context(self, data_dict: Dict[str, None | Dict], owner: str = "Unknown"):
        for plate, plate_violation_dict in data_dict.items():
            plate_info_dict = {"plate": plate, "owner": owner}
            plate_info_model = PlateInfoContextModel(**plate_info_dict)
            plate_info_model.get_plate_info(plate, plate_violation_dict)
            self.plates.append(plate_info_model)


__all__ = ["PlatesContextModel"]
