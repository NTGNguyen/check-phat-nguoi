from typing import Dict

from check_phat_nguoi.models.context import PlatesContextModel
from check_phat_nguoi.utils.singleton import Singleton


class PlatesContext(Singleton, PlatesContextModel):
    def get_context(self, data_dict: Dict[str, None | Dict], owner: str = "Unknown"):
        for plate, plate_violation_dict in data_dict.items():
            plate_info_dict = {"plate": plate, "owner": owner}
            plate_info_model = PlateInfoContextModel(**plate_info_dict)
            plate_info_model.get_plate_info(plate, plate_violation_dict)
            self.plates.append(plate_info_model)


plates_context: PlatesContext = PlatesContext()


__all__ = ["PlatesContext", "plates_context"]
