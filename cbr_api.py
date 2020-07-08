import requests
import xml.etree.ElementTree as ET
from models import CurrencyRate, peewee_datetime
from config import logging, LOGGER_CONFIG


log = logging.getLogger("CbrApi")
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
    currency_rate.rate = get_cbr_rate()
    currency_rate.updated = peewee_datetime.datetime.now()
    currency_rate.save()

    log.debug("Rate after: {}".format(currency_rate))
    log.info("Finished update for: {}=>{}".format(from_currency, to_currency))


def get_cbr_rate():
    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
    response_text = response.text
    log.debug("CBR response encoding: {}".format(response.encoding))
    log.debug("CBR response text: {}".format(response_text))
    usd_rate = find_usd_rate(response_text)

    return usd_rate


def find_usd_rate(response_text):
    root = ET.fromstring(response_text)
    valutes = root.findall("Valute")
    for valute in valutes:
        if valute.find('CharCode').text == "USD":
            return float(valute.find('Value').text.replace(",", "."))
    log.error("Invalid CBR response: USD not found")
    raise ValueError("Invalid CBR response: USD not found")
