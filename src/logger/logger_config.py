# config.py
def load_config():
    return {
        "version": 1,
        "formatters": {
            "brief": {
                "format": "%(asctime)s | %(relativeCreated)i | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
                "datefmt": "%Y-%j-%H%M%S",
                "style": "%",
            },
            "precise": {
                "format": "%(relativeCreated)i | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s",
                "datefmt": "%Y-%j-%H%M%S",
                "style": "%",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "brief",
                "level": "INFO",
                "filters": [],
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "precise",
                "level": "DEBUG",
                "filename": "/logs/log_file.log",
                "maxBytes": 1024,
                "backupCount": 5,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",  # parent level -> handler level hierarchy (logger is gatekeeper, but doesn't override)
        },
    }


# import generation
if __name__.endswith("config"):
    config = load_config()

# test config.py
if __name__ == "__main__":
    config = load_config()
    print(config)
