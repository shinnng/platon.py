from platon import Web3
from platon.providers.auto import (
    load_provider_from_uri,
)

from .endpoints import (
    INFURA_ROPSTEN_DOMAIN,
    build_http_headers,
    build_infura_url,
)

_headers = build_http_headers()
_infura_url = build_infura_url(INFURA_ROPSTEN_DOMAIN)

w3 = Web3(load_provider_from_uri(_infura_url, _headers))