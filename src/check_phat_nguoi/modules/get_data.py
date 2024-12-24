"""Get data"""

from logging import getLogger
from threading import Thread
from typing import Dict

import requests
from requests import Response

from check_phat_nguoi.models.config.plate_info import PlateInfoModel
from check_phat_nguoi.utils.constants import URL

logger = getLogger(__name__)


class GetData:
    """Get data by sending a request"""

    def __init__(self, plate_infos: list[PlateInfoModel]) -> None:
        """The initialise for GetData class

        Args:
            plate_infos: List of PlateInfo
        """
        self._plate_infos: list[PlateInfoModel] = plate_infos
        self.data_dict: Dict[str, None | Dict] = {}

    def _get_data(self, plate: str, timeout: int = 5) -> None:
        """Get data with a single object

        Args:
            plate: plate's information
            timeout: maximum wait time in seconds(default is 5)

        Returns:
            None | Dict: a dict
        """
        payload: dict[str, str] = {"bienso": f"{plate}"}
        try:
            response: Response = requests.post(url=URL, json=payload, timeout=timeout)
            response.raise_for_status()

            logger.info(f"Request successful: {response.status_code}")

            response_data: Dict = response.json()
            if response_data.get("data") is None:
                self.data_dict[plate] = None
            else:
                self.data_dict[plate] = response_data
        except requests.exceptions.ConnectionError:
            logger.error(f"Unable to connect to {URL}")
        except requests.exceptions.Timeout:
            logger.error(f"Time out of {timeout} seconds from URL {URL}")

    def get_data(self) -> Dict[str, None | Dict]:
        """Get data

        Returns:
            Dict: A dictionary mapping plate to response data.
        """
        threads: list[Thread] = []
        for plate_info in self._plate_infos:
            thread = Thread(target=self._get_data, args=(plate_info.plate,))
            threads.append(thread)
            thread.start()
        for idx, thread in enumerate(threads, start=1):
            try:
                thread.join()
            except Exception:
                logger.error(f"An error occurs in thread number {idx}")
        return self.data_dict
