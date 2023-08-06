from typing import cast, Iterator, Optional

from .access_tokens import get_access_token
from .config import DATA_URL, STATIONS_URL
from .interfaces import (
    DataFile,
    GetDataQuery,
    GetStationsQuery,
    PostDataPayload,
    RefreshToken,
    Station,
)
from .make_paginated_request import make_paginated_request
from .make_request import make_request


class Client():
    def __init__(
        self,
        refresh_token: RefreshToken,
        platform: str,
    ) -> None:
        self.refresh_token = refresh_token
        self.platform = platform

    def get_stations(
        self,
        query: Optional[GetStationsQuery] = None,
        *,
        page_size: int = 100,
    ) -> Iterator[Station]:
        access_token = get_access_token(
            refresh_token=self.refresh_token,
            platform=self.platform,
            scope='read:stations',
        )

        result = make_paginated_request(
            url=STATIONS_URL,
            token=access_token,
            query=query or {},
            page_size=page_size,
        )

        return cast(Iterator[Station], result)

    def get_data(
        self,
        query: Optional[GetDataQuery] = None,
        *,
        page_size: int = 100,
    ) -> Iterator[DataFile]:
        access_token = get_access_token(
            refresh_token=self.refresh_token,
            platform=self.platform,
            scope='read:data',
        )

        result = make_paginated_request(
            url=DATA_URL,
            token=access_token,
            query=query or {},
            page_size=page_size,
        )

        return cast(Iterator[DataFile], result)

    def post_data(
        self,
        payload: PostDataPayload,
    ) -> None:
        access_token = get_access_token(
            refresh_token=self.refresh_token,
            platform=self.platform,
            scope='write:data',
        )

        make_request(
            url=DATA_URL,
            token=access_token,
            method='POST',
            body=payload,
        )
