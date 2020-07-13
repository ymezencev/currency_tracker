from peewee import (SqliteDatabase, Model, CharField, IntegerField, DoubleField, DateTimeField, TextField,
                    datetime as peewee_datetime)
import config
db = SqliteDatabase(config.DB_NAME)


class _Model(Model):
    class Meta:
        database = db


class CurrencyRate(_Model):
    class Meta:
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


class ApiLog(_Model):
    class Meta:
        db_table = "api_logs"

    request_url = CharField()
    request_data = TextField(null=True)
    request_method = CharField(max_length=100)
    request_headers = TextField(null=True)
    response_text = TextField(null=True)
    created = DateTimeField(index=True, default=peewee_datetime.datetime.now)
    finished = DateTimeField()
    error = TextField(null=True)


class ErrorLog(_Model):
    class Meta:
        db_table = "error_logs"

    request_url = TextField(null=True)
    request_data = TextField(null=True)
    request_method = CharField(max_length=100, null=True)
    error = TextField()
    traceback = TextField(null=True)
    created = DateTimeField(index=True, default=peewee_datetime.datetime.now)


def init_db():
    CurrencyRate.drop_table()
    CurrencyRate.create_table()
    CurrencyRate.create(from_currency=840, to_currency=980, rate=1)
    CurrencyRate.create(from_currency=840, to_currency=643, rate=1)

    for m in (ApiLog, ErrorLog):
        m.drop_table()
        m.create_table()

    print("DB created!")


if __name__ == "__main__":
    init_db()
