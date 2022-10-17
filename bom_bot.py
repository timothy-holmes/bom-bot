import json

from src.logger import log
from src.bom_bot import BomETL



def main():
    with open("./config/config.json", "r") as c:
        config = json.load(c)
    log.debug("Loaded config file")

    with open("./config/stations.json", "r") as s:
        stations = json.load(s)
    log.debug("Loaded stations file")

    bom_etl = BomETL(config, stations)
    bom_etl.action_stations()
    log.debug("Extracted stations: {', '.join(s['station_name'] for s in stations}")



if __name__ == "__main__":
    main()
