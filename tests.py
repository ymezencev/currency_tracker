import unittest
import models
import test_api
import privat_api
import cbr_api


class Test(unittest.TestCase):
    def setUp(self):  # запускается перед каждым вызовом test_..
        models.init_db()

    def test_main(self):
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.0)
        test_api.update_currency_rate(840, 980)
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.01)

    def test_privat(self):
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.0)
        privat_api.update_currency_rate(840, 980)
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertGreater(currency_rate.rate, 25) # проверим, что курс больше 25

    def test_cbr(self):
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.0)
        cbr_api.update_currency_rate(840, 980)
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertGreater(currency_rate.rate, 60) # проверим, что курс больше 60