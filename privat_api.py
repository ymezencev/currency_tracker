import requests
from models import CurrencyRate, peewee_datetime
from config import logging, LOGGER_CONFIG


log = logging.getLogger("PrivatApi")
fh = logging.FileHandler(LOGGER_CONFIG["file"])
fh.setLevel(LOGGER_CONFIG["level"])
fh.setFormatter(LOGGER_CONFIG["formatter"])
log.addHandler(fh)
log.setLevel(LOGGER_CONFIG["level"])


def update_currency_rate(from_currency, to_currency):
    log.info("Started update for {}=>{}".format(from_currency, to_currency))
    currency_rate = CurrencyRate.select().where(CurrencyRate.from_currency == from_currency,
                                                CurrencyRate.to_currency == to_currency).first()

    log.debug("rate before: {}".format(currency_rate))
    currency_rate.rate = get_privat_rate()
    currency_rate.updated = peewee_datetime.datetime.now()
    currency_rate.save()

    log.debug("Rate after: {}".format(currency_rate))
    log.info("Finished update for: {}=>{}".format(from_currency, to_currency))


def get_privat_rate():
    response = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
    response_json = response.json()
    log.debug("Privat response: {}".format(response_json))
    usd_rate = find_usd_rate(response_json)

    return usd_rate


def find_usd_rate(response_json):
    for value in response_json:
        if value["ccy"] == "USD":
            return float(value["sale"])
    log.error("Invalid response: USD not found")
    raise ValueError("Invalid response: USD not found")
