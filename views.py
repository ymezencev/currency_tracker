from app import app
import controllers
from flask import request


@app.route("/hello")
def hello():
	return "Hello everybody!"


@app.route("/currency_rates")
def view_all_rates():
	return controllers.ViewAllRates().call()


@app.route("/api/rates/<fmt>")
def api_rates(fmt):
	return controllers.GetApiRates().call(fmt)


@app.route("/update/<int:from_currency>/<int:to_currency>")
@app.route("/update/all")
def update_rates(from_currency=None, to_currency=None):
	return controllers.UpdateApiRates().call(from_currency, to_currency)


@app.route("/logs")
def view_logs():
	return controllers.ViewLogs().call()
