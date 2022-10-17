import json
from typing import Any

import requests

from src.logger import log
from models import IotRecord, parse_bom_dt


class BomETL:
    def __init__(self, config: dict[str, str | str], stations: list[dict[str, str]]):
        # {"station_name": "TestStation", "station_url": "http://test"}
        self.stations = stations
        self.config = config
        log.info("Loaded `stations` and `config`")
        self.req = requests.Session()
        self.req.headers.update(config.get("req_headers"))
        log.debug(
            "Set request headers: "
            + ",".join(k for k in config.get("req_headers",{}))
        )
        log.info("BomScraper instance: ready")


    def action_stations(self):  # I hate myself
        for num, station in enumerate(self.stations):
            s_id = station["station_id"]
            s_name = station["station_name"]
            s_url = station["station_url"]

            # extract
            result, data = self._extract(num, s_id, s_name, s_url)
            log.info(f"{num}: Extracted station data: " + json.dumps(result))

            # transform
            records = self._transform(data)

            # load
            print(self._load(records))

    def _extract(self, num: int, s_id: str, s_name: str, s_url: str) -> tuple[dict[str ,str], list[dict[str, Any]]]:
        try:
            r = self.req.get(s_url)
            log.debug(f"Requested {s_url}, got {r.status_code=}")
            assert r.status_code == 200
        except Exception as e1:
            try:
                e = f"{num}: HTTPError/{e1}: {r.status_code=}, {r.content=}"
                log.error(e)
            except Exception as e2:
                e = f"{num}: ConnectionError/{e1}, {e2}: {s_url=}"
                log.error(e)
            return {"station_name": s_name, "error": e}, []

        try:
            s_json: dict = r.json()
            assert s_id == "{}.{}".format(
                    (s_json
                        .get("observations", {})
                        .get("data", [{}])[0]
                        .get("history_product", {})),
                    (s_json
                        .get("observations", {})
                        .get("data", [{}])[0]
                        .get("wmo", {}))
                )
        except Exception as e1:
            try:
                e = f"{num}: JSON/data error/{e1}: {r.status_code=}, {s_id} {r.content[:500]=}"
                log.error(e)
            except Exception as e2:
                e = f"{num}: JSON/data error/{e1}, {e2}: {r.status_code=}, {r.content[:500]=}"
                log.error(e)
            return {"station_name": s_name, "error": e}, []

        last_date_time: str = (
            s_json
                .get("observations", {})
                .get("data", [{}])[0]
                .get("local_date_time_full", {})
        )

        s_path = self.config.get("save_path","").format(
            station_name=s_name, last_date_time=last_date_time
        )  # prone to change

        with open(s_path, "w") as station_json_file:
            json.dump(s_json, station_json_file, indent=4)

        result: dict[str, str] = {"station_name": s_name, "last_date_time": last_date_time}
        data: list[dict[str, Any]] = s_json.get("observations", {}).get("data",[{}])

        return result, data
    
    def _transform(self, data: list[dict[str, Any]]) -> list[IotRecord]:
        records = []
        extend = records.extend
        for d in data:
            extend((
                IotRecord(
                    utc_dt = parse_bom_dt(d['aifstime_utc']),
                    device_id = f"{d['history']}.{d['wmo']}",
                    entry_type = "air_temp",
                    entry_frequency = "30m",
                    entry_value = d["air_temp"],
                    entry_unit = 'celcius'
                ),
                IotRecord(
                    utc_dt = parse_bom_dt(d['aifstime_utc']),
                    device_id = f"{d['history']}.{d['wmo']}",
                    entry_type = "apparent_t",
                    entry_frequency = "30m",
                    entry_value = d["apparent_t"],
                    entry_unit='celcius'
                )
            ))
        return records

    def _load(self, records: list[IotRecord]) -> dict[str, str | int]:
        return {'device_id': records[0].device_id, 'count': len(records)}

