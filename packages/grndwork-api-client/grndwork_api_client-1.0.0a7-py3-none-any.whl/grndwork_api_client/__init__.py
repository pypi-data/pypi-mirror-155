from .client import Client
from .config import get_refresh_token
from .interfaces import (
    DataFile,
    DataFileHeaders,
    DataRecord,
    GetDataQuery,
    GetStationsQuery,
    PostDataFile,
    PostDataPayload,
    RefreshToken,
    Station,
    StationDataFile,
)
from .make_request import RequestError

LOGGERNET_PLATFORM = 'loggernet'
TRACE_PLATFORM = 'trace'


def create_client(platform: str = LOGGERNET_PLATFORM) -> Client:
    return Client(
        refresh_token=get_refresh_token(),
        platform=platform,
    )


__all__ = [
    # Api client
    'create_client',
    'Client',

    # Platform constants
    'LOGGERNET_PLATFORM',
    'TRACE_PLATFORM',

    # Interfaces
    'DataFile',
    'DataFileHeaders',
    'DataRecord',
    'GetDataQuery',
    'GetStationsQuery',
    'PostDataFile',
    'PostDataPayload',
    'RefreshToken',
    'Station',
    'StationDataFile',

    # Errors
    'RequestError',
]
