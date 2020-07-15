import logging

DB_NAME = "currency_tracker.db"

LOGGER_CONFIG = dict(level=logging.DEBUG,
                     file="app.log",
                     formatter=logging.Formatter("%(asctime)s [%(levelname)s] - %(name)s:%(message)s"))

HTTP_TIMEOUT =15
