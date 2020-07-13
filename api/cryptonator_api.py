
from api import _Api


class Api(_Api):
    def __init__(self):
        super().__init__("CryptonatorApi")

    def _get_rate(self, from_currency, to_currency):
        crypt_aliases_map = {840: 'usd', 960: 'rub', 1000: "btc", 980: "uah"}

        if from_currency not in crypt_aliases_map or to_currency not in crypt_aliases_map:
            raise ValueError("Invalid from to currency: {}, {}".format(from_currency, to_currency))

        url_end = "{}-{}".format(crypt_aliases_map[from_currency], crypt_aliases_map[to_currency])
        url = "https://api.cryptonator.com/api/ticker/{}".format(url_end)

        response = self._send_request(url=url, method="get")
        self.log.debug("response status code {}".format(response.status_code))
        response_json = response.json()
        self.log.debug("Cryptonator response: {}".format(response_json))
        rate = self._find_rate(response_json)

        return rate

    def _update_rate(self, currency_rate):
        rate = self._get_rate(currency_rate.from_currency, currency_rate.to_currency)
        return rate

    def _find_rate(self, response_data):
        if "ticker" not in response_data:
            raise ValueError("Invalid crypronator responce: ticker not set")

        if "price" not in response_data:
            raise ValueError("Invalid crypronator responce: price not set")

        return float(response_data["ticker"]["price"])
