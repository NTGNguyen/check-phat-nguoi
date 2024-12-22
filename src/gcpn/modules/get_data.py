"""Get datas"""
import requests
import json
import threading
from requests import Response

from ..types.config import Config
from ..constants import URL

from typing import Dict


class _GetData:
    """Get data by sending a request"""

    def __init__(self, config: Config, url=URL) -> None:
        """The initialise for GetData class

        Args:
            config: config object
        """
        self._config: Config = config
        self._url = url

    def _get_data(self) -> None | Dict:
        """Get data with a single object

        Returns:
            None | Dict: _description_
        """
        payload: dict[str, str] = {
            "bienso": self._config.bien_so
        }
        try:
            response: Response = requests.post(
                url=self.url, json=payload)
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


class GetDataMultiThread():
    pass
