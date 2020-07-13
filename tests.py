import unittest
import json
from unittest.mock import patch
import requests
import models
import api


def get_privat_response(*args, **kwargs):
    class Response:
        def __init__(self, response):
            self.text = json.dumps(response)

        def json(self):
            return json.loads(self.text)

    return Response([{"ccy": "USD", "base_ccy": "UAH", "sale": "30.0"}])


class Test(unittest.TestCase):
    def setUp(self):  # запускается перед каждым вызовом test_..
        models.init_db()

    def test_privat_usd(self):
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.0)
        api.update_rate(840, 643)
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertGreater(currency_rate.rate, 25)  # проверим, что курс больше 25

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(api_log.response_text)

        self.assertIn('{"ccy":"USD","base_ccy":"UAH"', api_log.response_text)

    def test_privat_btc(self):
        currency_rate = models.CurrencyRate.get(from_currency=1000, to_currency=840)
        self.assertEqual(currency_rate.rate, 1.0)
        api.update_rate(1000, 840)
        currency_rate = models.CurrencyRate.get(from_currency=1000, to_currency=840)
        self.assertGreater(currency_rate.rate, 5000)  # проверим, что курс больше 25

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(api_log.response_text)

    def test_cbr(self):
        currency_rate = models.CurrencyRate.get(from_currency=840, to_currency=980)
        self.assertEqual(currency_rate.rate, 1.0)
        api.update_rate(840, 980)
        currency_rate = models.CurrencyRate.get(from_currency=840, to_currency=980)
        self.assertGreater(currency_rate.rate, 25)  # проверим, что курс больше 60

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "http://www.cbr.ru/scripts/XML_daily.asp")
        self.assertIsNotNone(api_log.response_text)

        self.assertIn('<NumCode>840</NumCode>', api_log.response_text)

    @patch('api._Api._send', new=get_privat_response)
    def test_privat_mock(self):

        currency_rate = models.CurrencyRate.get(id=1)
        updated_before = currency_rate.dt_updated
        self.assertEqual(currency_rate.rate, 1.0)

        api.update_rate(840, 643)

        currency_rate = models.CurrencyRate.get(id=1)
        updated_after = currency_rate.dt_updated

        self.assertEqual(currency_rate.rate, 30.0)
        self.assertGreater(updated_after, updated_before)

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(api_log.response_text)

        self.assertEqual('[{"ccy": "USD", "base_ccy": "UAH", "sale": "30.0"}]', api_log.response_text)

    def test_api_error(self):
        api.HTTP_TIMEOUT = 0.0001

        currency_rate = models.CurrencyRate.get(id=1)
        updated_before = currency_rate.dt_updated
        self.assertEqual(currency_rate.rate, 1.0)

        self.assertRaises(requests.exceptions.RequestException, api.update_rate, 840, 643)
        currency_rate = models.CurrencyRate.get(id=1)
        updated_after = currency_rate.dt_updated

        self.assertEqual(currency_rate.rate, 1.0)
        self.assertEqual(updated_after, updated_before)

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertEqual(api_log.request_url, "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNone(api_log.response_text)
        self.assertIsNotNone(api_log.error)

        error_log = models.ErrorLog.select().order_by(models.ErrorLog.created.desc()).first()
        self.assertIsNotNone(error_log)
        self.assertEqual(error_log.request_url, "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11")
        self.assertIsNotNone(error_log.error)
        self.assertIsNotNone(error_log.traceback)
        self.assertEqual(api_log.error, error_log.error)
        self.assertIn("Connection to api.privatbank.ua timed out", error_log.error)

        api.HTTP_TIMEOUT = 15

    def test_cryptonator_api(self):
        currency_rate = models.CurrencyRate().get(from_currency=960, to_currency=1000)
        updated_before = currency_rate.dt_updated
        self.assertEqual(currency_rate.rate, 1.0)

        api.update_rate(960, 1000)

        currency_rate = models.CurrencyRate.get(from_currency=960, to_currency=1000)
        updated_after = currency_rate.dt_updated

        self.assertGreater(currency_rate.rate, 1000.0)
        self.assertGreater(updated_after, updated_before)

        api_log = models.ApiLog.select().order_by(models.ApiLog.created.desc()).first()
        self.assertIsNotNone(api_log)
        self.assertIsNotNone(api_log.response_text)
