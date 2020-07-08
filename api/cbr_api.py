import xml.etree.ElementTree as ET
from api import _Api
import requests


class Api(_Api):
    def __init__(self):
        super().__init__("CbrApi")

    def _update_rate(self, currency_rate):
        rate = self._get_cbr_rate(currency_rate.from_currency)
        return rate

    def _get_cbr_rate(self, from_currency):
        response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
        response_text = response.text

        self.log.debug("CBR response encoding: {}".format(response.encoding))
        self.log.debug("CBR response text: {}".format(response_text))
        usd_rate = self._find_rate(response_text, from_currency)

        return usd_rate

    def _find_rate(self, response_text, from_currency):
        root = ET.fromstring(response_text)
        valutes = root.findall("Valute")

        cbr_valute_map = {840: 'USD', 960: 'RUB'}

        for valute in valutes:
            if valute.find('CharCode').text == cbr_valute_map[from_currency]:
                return float(valute.find('Value').text.replace(",", "."))
        self.log.error("Invalid CBR response: Currency {} not found".format(cbr_valute_map[from_currency]))
        raise ValueError("Invalid CBR response: Currency {} not found".format(cbr_valute_map[from_currency]))
