from typing import Any, Iterator, MutableMapping, Optional

from .content_range import ContentRange
from .make_request import make_request


def make_paginated_request(
    url: str,
    *,
    token: str,
    headers: Optional[MutableMapping[str, Any]] = None,
    query: Any = None,
    page_size: int = 100,
) -> Iterator[Any]:
    headers = headers or {}
    query = query or {}
    limit = query.get('limit')
    offset = query.get('offset') or 0

    while True:
        results, headers = make_request(
            url=url,
            token=token,
            headers=headers,
            query={
                **query,
                'limit': min(limit, page_size) if limit else page_size,
                'offset': offset,
            },
        )

        yield from results

        if limit:
            limit -= len(results)

            if limit <= 0:
                break

        content_range = ContentRange.parse(headers.get('Content-Range') or '')

        if offset < content_range.last:
            offset = content_range.last

            if offset >= content_range.count:
                break
        else:
            raise ValueError('Invalid content range')
