from pydantic import BaseModel

from check_phat_nguoi.models.context.plate_info import PlateInfoModel

from typing import Dict


class ContextModel(BaseModel):
    data: list[PlateInfoModel] = []

    def get_context(self, data_dict: Dict[str, None | Dict], owner: str = "Unknown"):
        for plate, plate_violation_dict in data_dict.items():
            plate_info_dict = {"plate": plate, "owner": owner}
            plate_info_model = PlateInfoModel(**plate_info_dict)
            plate_info_model.get_plate_info(plate, plate_violation_dict)
            self.data.append(plate_info_model)


__all__ = ["ContextModel"]
