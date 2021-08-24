import logging
from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
    Tuple,
    Union,
)

from platon_typing import (
    URI,
)
from platon_utils import (
    to_dict,
)

from platon._utils.http import (
    construct_user_agent,
)
from platon._utils.request import (
    async_make_post_request,
    get_default_http_endpoint,
)
from platon.types import (
    RPCEndpoint,
    RPCResponse,
)

from .async_base import (
    AsyncJSONBaseProvider,
)


class AsyncHTTPProvider(AsyncJSONBaseProvider):
    logger = logging.getLogger("platon.providers.HTTPProvider")
    endpoint_uri = None
    _request_kwargs = None

    def __init__(
        self, endpoint_uri: Optional[Union[URI, str]] = None,
            request_kwargs: Optional[Any] = None
    ) -> None:
        if endpoint_uri is None:
            self.endpoint_uri = get_default_http_endpoint()
        else:
            self.endpoint_uri = URI(endpoint_uri)

        self._request_kwargs = request_kwargs or {}

        super().__init__()

    def __str__(self) -> str:
        return "RPC connection {0}".format(self.endpoint_uri)

    @to_dict
    def get_request_kwargs(self) -> Iterable[Tuple[str, Any]]:
        if 'headers' not in self._request_kwargs:
            yield 'headers', self.get_request_headers()
        for key, value in self._request_kwargs.items():
            yield key, value

    def get_request_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'User-Agent': construct_user_agent(str(type(self))),
        }

    async def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        self.logger.debug("Making request HTTP. URI: %s, Method: %s",
                          self.endpoint_uri, method)
        request_data = self.encode_rpc_request(method, params)
        raw_response = await async_make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Method: %s, Response: %s",
                          self.endpoint_uri, method, response)
        return response