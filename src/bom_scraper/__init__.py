import json
import requests

class BomScraper:
    def __init__(self, config: dict[str, str],  stations: list[dict[str, str]]):
        self.config = config

        # {"station_name": "Test", "station_url": "http://test"}
        self.stations = stations


    def action_stations(self): # I hate myself
        for station in self.stations:
            response = requests.get("https://stackoverflow.com/questions/31126596/saving-response-from-requests-to-file")
            with open("response.txt", "w") as f:
                f.write(response.text)