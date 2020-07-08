import requests
import xml.etree.ElementTree as ET
from models import CurrencyRate, peewee_datetime
from config import logging, LOGGER_CONFIG


class _Api:
    def __init__(self, logger_name):

        self.log = logging.getLogger(logger_name)
        fh = logging.FileHandler(LOGGER_CONFIG["file"])
        fh.setLevel(LOGGER_CONFIG["level"])
        fh.setFormatter(LOGGER_CONFIG["formatter"])
        self.log.addHandler(fh)
        self.log.setLevel(LOGGER_CONFIG["level"])

    def update_rate(self, from_currency, to_currency):

        self.log.info("Started update for {}=>{}".format(from_currency, to_currency))

        currency_rate = CurrencyRate.select().where(CurrencyRate.from_currency == from_currency,
                                                    CurrencyRate.to_currency == to_currency).first()

        self.log.debug("rate before: {}".format(currency_rate))
        currency_rate.rate = self._update_rate(currency_rate)
        currency_rate.dt_updated = peewee_datetime.datetime.now()
        currency_rate.save()

        self.log.debug("Rate after: {}".format(currency_rate))
        self.log.info("Finished update for: {}=>{}".format(from_currency, to_currency))

    def _update_rate(self, currency_rate):
        raise NotImplementedError("_update_rate")
