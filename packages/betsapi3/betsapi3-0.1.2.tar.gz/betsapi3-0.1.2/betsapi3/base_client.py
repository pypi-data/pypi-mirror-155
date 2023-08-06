from abc import ABC
from dataclasses import dataclass
from typing import ClassVar
from urllib.parse import urljoin

import requests
from requests import Response

from betsapi3.utils import Endpoint


@dataclass(slots=True)
class BaseAPIClient(ABC):
    api_key: str  # API key provided by bets365
    _base_url: ClassVar[str] = 'https://api.b365api.com'
    _endpoints: ClassVar[dict[str, Endpoint]] = {}

    def _make_request(self, endpoint_name: str, **kwargs) -> Response:
        return requests.get(self._get_endpoint(endpoint_name, **kwargs))

    def _get_endpoint(self, endpoint_name: str, **kwargs) -> str:
        endpoint: Endpoint = self._endpoints[endpoint_name]

        return urljoin(self._base_url, endpoint.to_url(self.api_key if endpoint.token_is_required else None, **kwargs))
