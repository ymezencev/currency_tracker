from peewee import (SqliteDatabase, Model, IntegerField, DoubleField, DateTimeField, datetime as peewee_datetime)
import config
db = SqliteDatabase(config.DB_NAME)


class CurrencyRate(Model):
    class Meta:
        database = db
        db_table = "rates"
        indexes = (
            (("from_currency", "to_currency"), True),
        )

    from_currency = IntegerField()
    to_currency = IntegerField()
    rate = DoubleField()
    dt_updated = DateTimeField(default=peewee_datetime.datetime.now)

    def __str__(self):
        return "CurrencyRate(%s=>%s): %s" % (self.from_currency, self.to_currency, self.rate)


def init_db():
    db.drop_tables(CurrencyRate)
    CurrencyRate.create_table()
    CurrencyRate.create(from_currency=840, to_currency=980, rate=1)
    print("DB created!")


if __name__ == "__main__":
    init_db()
