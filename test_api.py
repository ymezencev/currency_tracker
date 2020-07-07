from models import CurrencyRate


def update_currency_rate(from_currency, to_currency):
    currency_rate = CurrencyRate.select().where(CurrencyRate.from_currency == from_currency,
                                                CurrencyRate.to_currency == to_currency).first()

    print("Rate before: ", currency_rate)
    currency_rate.rate += 0.01
    currency_rate.save()
    print("Rate after: ", currency_rate)


if __name__ == "__main__":
    update_currency_rate(840, 980)
