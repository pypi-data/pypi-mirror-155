from dataclasses import dataclass, field
from typing import Callable, Any, Dict

from requests import Response


@dataclass(slots=True)
class UrlParameter:
    type: type
    required: bool = False


@dataclass(slots=True)
class Endpoint:
    name: str
    version: int
    api_name: str
    url_parameters: dict[str, UrlParameter] = field(default_factory=dict)
    token_is_required: bool = True

    def to_url(self, token: str | None = None, **kwargs) -> str:
        if self.token_is_required and token is None:
            raise Exception('Token is required!')

        url: str = f'/v{self.version}/{self.api_name}/{self.name}'
        for name, url_parameter in self.url_parameters.items():
            if url_parameter.required and not kwargs.get(name):
                raise Exception(f'Required argument missing {name}')

        for i, (parameter, value) in enumerate(kwargs.items()):
            try:
                url_parameter: UrlParameter = self.url_parameters[parameter]
                if not url_parameter.required and value is None and url_parameter.type is not None:
                    continue
                if url_parameter.type is not type(value):
                    raise Exception('Url Parameter Value is not correct!')
            except KeyError:
                raise Exception('Unexpected Parameter for this endpoint')

            url += f'{"?" if i == 0 else "&"}{parameter}={value}'
        if self.token_is_required:
            url += f'{"?" if url.endswith(self.name) else "&"}token={token}'

        return url


def api_endpoint(func: Callable[[Any, Any], Response]):
    def wrapper(*args, **kwargs) -> Response:
        if len(args) == 0:
            raise Exception('Self parameter is missing!')

        self = args[0]
        # Transform args to kwargs
        possible_kwargs = func.__code__.co_varnames[1:]
        for i, arg in enumerate(args[1:]):
            kwargs[possible_kwargs[i]] = arg

        return self._make_request(func.__name__, **kwargs)

    return wrapper
