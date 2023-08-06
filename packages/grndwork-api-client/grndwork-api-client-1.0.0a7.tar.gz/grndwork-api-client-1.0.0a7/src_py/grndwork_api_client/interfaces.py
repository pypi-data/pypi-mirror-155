from typing import Any, Dict, List, Optional, TypedDict


class RefreshToken(TypedDict):
    subject: str
    token: str


class DataRecord(TypedDict):
    timestamp: str
    record_num: int
    data: Dict[str, Any]


class DataFileHeaders(TypedDict):
    meta: Optional[Dict[str, Any]]
    columns: List[str]
    units: List[str]
    processing: List[str]


class DataFile(TypedDict):
    source: str
    filename: str
    is_stale: bool
    headers: DataFileHeaders
    records: List[DataRecord]


class StationDataFile(TypedDict):
    filename: str
    is_stale: bool
    headers: DataFileHeaders


class Station(TypedDict):
    client_uuid: str
    client_full_name: str
    client_short_name: str
    site_uuid: str
    site_full_name: str
    station_uuid: str
    station_full_name: str
    description: str
    latitude: int
    longitude: int
    altitude: int
    timezone_offset: Optional[int]
    start_timestamp: Optional[str]
    end_timestamp: Optional[str]
    data_file_prefix: str
    data_files: List[StationDataFile]


class GetStationsQuery(TypedDict):
    client: Optional[str]
    site: Optional[str]
    station: Optional[str]
    limit: Optional[int]
    offset: Optional[int]


class GetDataQuery(TypedDict):
    client: Optional[str]
    site: Optional[str]
    gateway: Optional[str]
    station: Optional[str]
    filename: Optional[str]
    limit: Optional[int]
    offset: Optional[int]
    records_before: Optional[str]
    records_after: Optional[str]
    records_limit: Optional[str]


class PostDataFile(TypedDict):
    filename: str
    headers: Optional[DataFileHeaders]
    records: Optional[List[DataRecord]]


class PostDataPayload(TypedDict):
    source: str
    files: List[PostDataFile]
    overwrite: Optional[bool]
