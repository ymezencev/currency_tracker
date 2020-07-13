import requests
import traceback
import importlib

import xml.etree.ElementTree as ET
from models import CurrencyRate, ApiLog, ErrorLog, peewee_datetime
from config import logging, LOGGER_CONFIG, HTTP_TIMEOUT


def update_rate(from_currency, to_currency):
    currency_rate = CurrencyRate.select().where(CurrencyRate.from_currency == from_currency,
                                                CurrencyRate.to_currency == to_currency).first()
    module = importlib.import_module("api.{}".format(currency_rate.module))
    module.Api().update_rate(currency_rate.from_currency, to_currency)


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

    def _send_request(self, url, method, data=None, headers=None):
        log = ApiLog(request_url=url, request_data=data, request_method=method, request_headers=headers)

        try:
            response = self._send(method=method, url=url, headers=headers, data=data)
            log.response_text = response.text
            return response

        except Exception as ex:
            self.log.exception("Error during request sending")
            log.error = str(ex)
            ErrorLog.create(request_data=data, request_url=url, requst_method=method,
                            error=str(ex), traceback=traceback.format_exc(chain=False))
            raise
        finally:
            log.finished = peewee_datetime.datetime.now()
            log.save()

    def _send(self, url, method, data=None, headers=None):
        return requests.request(method=method, url=url, headers=headers, data=data, timeout=HTTP_TIMEOUT)

