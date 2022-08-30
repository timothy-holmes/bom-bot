import json
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

from src.logger import build_logger

logger = build_logger(".".join(["bom-bot", __name__]))

# not used yet
class CustomException:
    def __init__(self, exception_raised):
        logger.error(f"{str(exception_raised)=}")
        raise Exception


class BomScraper:
    def __init__(self, config: dict[str, str], stations: list[dict[str, str]]):
        # {"station_name": "TestStation", "station_url": "http://test"}
        self.stations = stations
        self.config = config
        logger.info("Loaded `stations` and `config`")
        self.req = requests.Session()
        self.req.headers.update(config.get("req_headers", None))
        logger.debug(
            "Set request headers: "
            + ",".join(k for k, v in config.get("req_headers", {}).items())
        )
        logger.info("BomScraper instance: ready")

    def action_stations(self):  # I hate myself
        results = {
            "start_time": str(datetime.now(tz=ZoneInfo("Australia/Melbourne"))),
            "stations": [],
        }

        for num, station in enumerate(self.stations):
            s_id = station["station_id"]
            s_name = station["station_name"]
            s_url = station["station_url"]

            try:
                r = self.req.get(s_url)
                assert r.status_code == 200
                logger.debug(f"Requested {s_url}, got {r.status_code=}")
            except Exception as e1:
                try:
                    logger.error(
                        f"{num}: HTTPError/{e1}: {r.status_code=}, {r.content=}"
                    )
                except Exception as e2:
                    logger.error(f"{num}: ConnectionError/{e1}, {e2}: {s_url=}")
                continue

            try:
                s_json = r.json()
                assert s_id == (
                    json_id := s_json.get("observations", {})
                    .get("header", [""])[0]
                    .get("ID", {})
                )
            except Exception as e1:
                try:
                    logger.error(
                        f"{num}: JSON/data error/{e1}: {r.status_code=}, {s_id}=={json_id} {r.content[:500]=}"
                    )
                except Exception as e2:
                    logger.error(
                        f"{num}: JSON/data error/{e1}, {e2}: {r.status_code=}, {r.content[:500]=}"
                    )
                continue

            last_date_time = (
                s_json.get("observations", {})
                .get("data", [""])[0]
                .get("local_date_time_full", {})
            )

            s_path = self.config.get("save_path").format(
                station_name=s_name, last_date_time=last_date_time
            )  # prone to change

            with open(s_path, "w") as station_json_file:
                json.dump(s_json, station_json_file, indent=4)

            result = {"station_name": s_name, "last_date_time": last_date_time}
            results["stations"].append(result)
            logger.info(f"{num}: Extracted station data: " + json.dumps(result))

        # return results
