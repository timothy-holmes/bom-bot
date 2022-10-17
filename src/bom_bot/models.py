from dataclasses import dataclass
from datetime import datetime


@dataclass
class IotRecord:
    """Class for keeping track of an item in inventory."""
    utc_dt: str               # yyyy-mm-ddThh:mm:ssZ ie. ISO-8601
    device_id: str
    entry_type: str
    entry_frequency: str
    entry_value: float
    entry_unit: str

def parse_bom_dt(utc_dt: str) -> str:
    return datetime.strftime(
        datetime.strptime(utc_dt,'%Y%m%d%H%M%S'),
        '%Y%m%dT%H%M%SZ'
    )