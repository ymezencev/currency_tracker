from models import CurrencyRate
from config import logging, LOGGER_CONFIG

log = logging.getLogger("TestApi")
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
    currency_rate.rate += 0.01
    currency_rate.save()
    log.debug("Rate after: {}".format(currency_rate))
    log.info("Finished update for: {}=>{}".format(from_currency, to_currency))


if __name__ == "__main__":
    update_currency_rate(840, 980)
