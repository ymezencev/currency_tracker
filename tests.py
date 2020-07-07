import unittest
import models
import test_api


class Test(unittest.TestCase):
    def setUp(self):  # запускается перед каждым вызовом test_..
        models.init_db()

    def test_main(self):
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.0)
        test_api.update_currency_rate(840, 980)
        currency_rate = models.CurrencyRate.get(id=1)
        self.assertEqual(currency_rate.rate, 1.01)
