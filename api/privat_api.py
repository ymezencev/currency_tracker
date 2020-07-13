import xml.etree.ElementTree as ET
from api import _Api
import requests


class Api(_Api):
    def __init__(self):
        super().__init__("PrivatApi")

    def _update_rate(self, currency_rate):
        rate = self._get_privat_rate(currency_rate.from_currency)
        return rate

    def _get_privat_rate(self, from_currency):
        response = self._send_request(url="https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
                                      method="get")
        response_json = response.json()
        self.log.debug("Privat response: {}".format(response_json))
        usd_rate = self._find_rate(response_json, from_currency)

        return usd_rate

    def _find_rate(self, response_json, from_currency):
        privat_aliases_map = {840: 'USD', 960: 'RUB', 1000: "BTC"}
        if from_currency not in privat_aliases_map:
            raise ValueError("Invalid from currency {}".format(from_currency))

        currency_alias = privat_aliases_map[from_currency]
        for value in response_json:
            if value["ccy"] == currency_alias:
                return float(value["sale"])
        self.log.error("Invalid Privat response: Currency {} not found".format(currency_alias))
        raise ValueError("Invalid Privat response: Currency {} not found".format(currency_alias))
