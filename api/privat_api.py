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
        response = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        response_json = response.json()
        self.log.debug("Privat response: {}".format(response_json))
        usd_rate = self._find_rate(response_json, from_currency)

        return usd_rate

    def _find_rate(self, response_json, from_currency):
        privat_valute_map = {840: 'USD', 960: 'RUB'}

        for value in response_json:
            if value["ccy"] == privat_valute_map[from_currency]:
                return float(value["sale"])
        self.log.error("Invalid Privat response: Currency {} not found".format(privat_valute_map[from_currency]))
        raise ValueError("Invalid Privat response: Currency {} not found".format(privat_valute_map[from_currency]))
