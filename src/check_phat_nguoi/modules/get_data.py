"""Get datas"""

import threading
from typing import Dict

import requests
from requests import Response

from check_phat_nguoi.models.plate_info import PlateInfo

from ..utils.constants import URL


class GetData:
    """Get data by sending a request"""

    def __init__(self, plate_infos: list[PlateInfo]) -> None:
        """The initialise for GetData class

        Args:
            plate_infos: List of PlateInfo
        """
        self._plate_infos = plate_infos

    def _get_data(self) -> None | Dict:
        """Get data with a single object

        Returns:
            None | Dict: _description_
        """
        # TODO: Iterate từng _plate_infos lấy biển plate nha Nguyễn
        payload: dict[str, str] = {"bienso": ""}
        try:
            response: Response = requests.post(url=URL, json=payload)
            response.raise_for_status()
            response_data: Dict = response.json()
            if response_data.get("data") is None:
                return None
            else:
                return response_data
        except:
            return None


class _GetDataThread(threading.Thread):
    pass


class GetDataMultiThread:
    pass
