import json
from src.bom_bot import BomScraper


def main():
    with open("./config/config.json", "r") as c:
        config = json.load(c)

    with open("./config/stations.json", "r") as s:
        stations = json.load(s)

    bom_scraper = BomScraper(config, stations)
    bom_scraper.action_stations()


if __name__ == "main":
    main()
