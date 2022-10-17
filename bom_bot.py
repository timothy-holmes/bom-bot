import json
from src.bom_bot import BomETL, build_logger


def main():
    logger = build_logger(".".join(["bom-bot", __name__]))
    logger.debug("Created logger")

    with open("./config/config.json", "r") as c:
        config = json.load(c)
    logger.debug("Loaded config file")

    with open("./config/stations.json", "r") as s:
        stations = json.load(s)
    logger.debug("Loaded stations file")

    bom_extract = BomETL(config, stations)
    extract = bom_extract.action_stations()
    logger.debug("Extracted stations: {', '.join(s['station_name'] for s in stations}")



if __name__ == "__main__":
    main()
