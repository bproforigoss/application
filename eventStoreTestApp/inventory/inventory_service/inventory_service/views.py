import prometheus_client
import requests
from flask import render_template, request, Response

from inventory_service import inventory_web_interface, app
from . import prom_logs

http_summary_metric = prom_logs.performance_metrics["http_request_summary"]


@app.route("/", methods=["GET"])
def inventory_process(error=None):
    inventory = {
        item.name: item.amount for item in inventory_web_interface.inventory.values()
    }
    return render_template("inventory_page.html", inventory=inventory, error=error)


@app.route("/create", methods=["POST"])
@http_summary_metric.time()
def create_product():
    name = request.form["name"]
    price = request.form["price"]
    currency = request.form["currency"]
    if name != "" and price != "" and currency != "":
        try:
            inventory_web_interface.create_product(
                {"name": name, "price": price, "currency": currency}
            )
        except requests.exceptions.RequestException:
            return inventory_process(
                "There was a problem connecting to the database services."
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/delete", methods=["POST"])
@http_summary_metric.time()
def delete_product():
    name = request.form["namedelete"]
    if name != "":
        try:
            inventory_web_interface.delete_product(name)
        except requests.exceptions.RequestException:
            return inventory_process(
                "There was a problem connecting to the database services."
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/add", methods=["POST"])
@http_summary_metric.time()
def add_stock_reroute():
    name = request.form["nameaddsubtract"]
    amount = request.form["amountaddsubtract"]
    if name != "" and amount != "":
        try:
            inventory_web_interface.increase_item_amount(name, amount)
        except requests.exceptions.RequestException:
            return inventory_process(
                "There was a problem connecting to the database services."
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/subtract", methods=["POST"])
@http_summary_metric.time()
def subtract_stock_reroute():
    name = request.form["nameaddsubtract"]
    amount = request.form["amountaddsubtract"]
    if name != "" and amount != "":
        try:
            inventory_web_interface.decrease_item_amount(name, amount)
        except requests.exceptions.RequestException:
            return inventory_process(
                "There was a problem connecting to the database services."
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/health", methods=["GET"])
def health_check():
    return Response({"health check": "successful"}, status=200)


@app.route("/metrics", methods=["GET"])
def metrics():
    readings = []
    for metric in prom_logs.performance_metrics.values():
        readings.append(prometheus_client.generate_latest(metric))
    readings.append(
        prometheus_client.generate_latest(prometheus_client.PROCESS_COLLECTOR)
    )
    return Response(readings, mimetype="text/plain")
