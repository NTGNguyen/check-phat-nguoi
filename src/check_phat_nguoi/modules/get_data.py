"""Get data"""

from threading import Thread
from typing import Dict

import requests
from requests import Response

from check_phat_nguoi.models.plate_info import PlateInfo
from check_phat_nguoi.utils.constants import URL


class GetData:
    """Get data by sending a request"""

    def __init__(self, plate_infos: list[PlateInfo]) -> None:
        """The initialise for GetData class

        Args:
            plate_infos: List of PlateInfo
        """
        self._plate_infos: list[PlateInfo] = plate_infos
        self.data_dict: Dict[str, None | Dict] = {}

    def _get_data(self, plate: str) -> None:
        """Get data with a single object

        Args:
            plate: plate's information

        Returns:
            None | Dict: a dict
        """
        payload: dict[str, str] = {"bienso": f"{plate}"}
        try:
            response: Response = requests.post(url=URL, json=payload)
            response.raise_for_status()
            response_data: Dict = response.json()
            if response_data.get("data") is None:
                self.data_dict[plate] = None
            else:
                self.data_dict[plate] = response_data
        except Exception:
            self._data_dict[plate] = None

    def get_data(self) -> Dict[str, None | Dict] | None:
        """Get data

        Returns:
            Dict: A dictionary mapping plate to response data.
        """

        threads: list[Thread] = []
        try:
            for plate_info in self._plate_infos:
                thread = Thread(target=self._get_data,
                                args=(plate_info.plate,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            return self.data_dict
        except Exception:
            return None
