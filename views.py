from functools import wraps
from app import app
import controllers
from config import IP_LIST
from flask import request, render_template, abort


def check_ip(func):
	@wraps(func)
	def checker(*args, **kwargs):
		if request.remote_addr not in IP_LIST:
			return abort(403)
		return func(*args, **kwargs)
	return checker


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
@check_ip
def view_logs():
	return controllers.ViewLogs().call()

@app.route("/edit/<int:from_currency>/<int:to_currency>", methods=["GET", 'POST'])
@check_ip
def edit_rates(from_currency, to_currency):
	return controllers.EditRate().call(from_currency, to_currency)