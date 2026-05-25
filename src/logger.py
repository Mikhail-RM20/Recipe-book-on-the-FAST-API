dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s | %(lineno)d",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "information_work_programm.log",
            "mode": "a",
        }
    },
    "loggers": {"main": {"level": "DEBUG", "handlers": ["file"]}},
}
