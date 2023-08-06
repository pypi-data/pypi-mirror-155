from http.client import responses as status_codes
import json
from typing import Any, List, MutableMapping, Optional, Tuple

import requests


class RequestError(Exception):
    def __init__(self, *args: Any, errors: Optional[List[Any]] = None) -> None:
        super().__init__(*args)
        self.errors = errors or []


def make_request(
    url: str,
    *,
    token: str,
    method: str = 'GET',
    headers: Optional[MutableMapping[str, Any]] = None,
    query: Any = None,
    body: Any = None,
) -> Tuple[Any, MutableMapping[str, Any]]:
    headers = headers or {}
    query = query or {}

    if token:
        headers['Authorization'] = f'Bearer {token}'

    if body:
        headers['Content-Type'] = 'application/json'

    resp = requests.request(
        url=url,
        method=method,
        headers=headers,
        params=query,
        data=json.dumps(body),
    )

    try:
        payload = resp.json()
    except requests.RequestException:
        raise RequestError('Failed to parse response payload')

    if resp.status_code >= 400:
        raise RequestError(
            payload.get('message') or status_codes[resp.status_code],
            errors=payload.get('errors'),
        )

    return payload, resp.headers
