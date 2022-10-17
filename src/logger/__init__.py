import json
import logging
import logging.config

"""
Setup:
    $ cat .gitmmodules
    [submodule "mini-logger"]
        path = logger
        url = https://github.com/timothy-holmes/mini-logger

    note: path not the same as repo name becuase repo name contains '-' character
          making imports in python difficult

Usage:
    Import in projects like so:
    1. Modify logger_config.py as required.
    2. Import module where required
        from submodules.logger import build_logger
    3. Generate logger, or pass it around, as necessary
        log = build_logger('.'.join([app_name,__name__]))

"""

with open("./config/logging.json", "r") as config_json:
    logging.config.dictConfig(json.load(config_json))

log = logging.getLogger('bom-bot')

def build_logger(name: str):
    log = logging.getLogger(name)
    return log


def logger_build_test():
    name = ".".join(["logger_test", __name__])
    log = build_logger(name)
    log.debug(f"Logger {name} created")
    log.warning("Log test works")


# test
if __name__ == "__main__":
    logger_build_test()
