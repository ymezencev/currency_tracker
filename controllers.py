from flask import render_template, make_response, jsonify, request, redirect, url_for
import xmltodict
from models import CurrencyRate, ApiLog
import api
import datetime

class BaseController:
	def __init__(self):
		self.request = request		

	def call(self, *args, **kwargs):
		try:
			return self._call(*args, **kwargs)		
		except Exception as ex:
			return make_response(str(ex), 500)

	def _call(self, *args, **kwargs):
		raise NotImplemetntedError("_call")


class ViewAllRates(BaseController):

	def _call(self):
		currency_rate = CurrencyRate.select()
		return render_template("currency_rates.html", currency_rate=currency_rate)


class GetApiRates(BaseController):

	def _call(self, fmt):
		currency_rate = CurrencyRate.select()
		currency_rate = self._filter(currency_rate)
		
		if fmt == "json":
			return self._get_json(currency_rate)
		elif fmt == "xml":
			return self._get_xml(currency_rate)
		else:
			raise ValueError(f"Unknown fmt {fmt}")

	def _filter(self, currency_rate):
		args = self.request.args

		if "from" in args:
			currency_rate = currency_rate.where(CurrencyRate.from_currency == args["from"])
		if "to" in args:
			currency_rate = currency_rate.where(CurrencyRate.to_currency == args["to"])

		return currency_rate

	def _get_json(self, currency_rate):
		return jsonify([{"from": rate.from_currency, "to": rate.to_currency, "rate": rate.rate} for rate in currency_rate])

	def _get_xml(self, currency_rate):
		d = {"currency_rates": {"currency_rate": [
					{"from": rate.from_currency, "to": rate.to_currency, "rate": rate.rate} for rate in currency_rate]}}
		return make_response(xmltodict.unparse(d), {"Content-Type": "text/xml"})


class UpdateApiRates(BaseController):

	def _call(self, from_currency, to_currency):
		if not from_currency and not to_currency:
			self._update_all()
		elif from_currency and to_currency:
			self._update_rate(from_currency, to_currency)
		else:
			raise ValueError("from currency and to_currency")
		return redirect("/currency_rates")

	def _update_rate(self, from_currency, to_currency):
		api.update_rate(from_currency, to_currency)

	def _update_all(self):
		currency_rates = CurrencyRate.select()
		for rate in currency_rates:
			try:
				self._update_rate(rate.from_currency, rate.to_currency)
			except Exception as ex:
				print(ex)


class ViewLogs(BaseController):
	def _call(self):
		page = int(self.request.args.get("page", 1))
		logs = ApiLog.select().paginate(page, 10).order_by(ApiLog.id.desc())
		return render_template("logs.html", logs=logs)


class EditRate(BaseController):

	def _call(self, from_currency, to_currency):
		if self.request.method == 'GET'	:
			return render_template("rate_edit.html", 
							from_currency=from_currency, 
							to_currency=to_currency)
		#  POST
		print(request.form)
		print(self.request.form)
		if "new_rate" not in self.request.form:
			raise Exception("new_rate parameter is required")

		if not self.request.form["new_rate"]:
		 	raise Exception("new_rate must not be empty")

		upd_count = (CurrencyRate.update({CurrencyRate.rate: float(self.request.form["new_rate"]),
		 								   CurrencyRate.dt_updated: datetime.datetime.now()}).where(
		 								     CurrencyRate.from_currency == from_currency,
		 								     CurrencyRate.to_currency == to_currency).execute())
		print("Update count: ", upd_count)
		return redirect(url_for('view_all_rates'))
