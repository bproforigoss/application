import prometheus_client
import requests
from flask import render_template, request, Response

from order_service import order_web_interface, app
from . import prom_logs

http_duration_metric = prom_logs.performance_metrics["http_request_summary"]


@app.route("/", methods=["GET"])
@http_duration_metric.time()
def order_process(error=None):
    return render_template("order_page.html", error=error)


@app.route("/create", methods=["POST"])
@http_duration_metric.time()
def create_order_session():
    try:
        created_id = order_web_interface.create_order_session()
        return render_template("order_created.html", id=created_id)
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


@app.route("/add", methods=["POST"])
@http_duration_metric.time()
def add_to_order():
    form = request.form
    try:
        if form["order_id"] != "" and form["item"] != "" and form["amount"] != "":
            order_web_interface.add_item(form["item"], form["amount"], form["order_id"])
            return render_template(
                "order_page.html",
                session_id=form["order_id"],
                item=form["item"],
                amount=form["amount"],
                added=True,
            )
        else:
            return order_process("Not all required filled")
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


@app.route("/delete", methods=["POST"])
@http_duration_metric.time()
def delete_from_order():
    form = request.form
    try:
        if form["order_id"] != "" and form["item"] != "":
            if order_web_interface.remove_item(form["item"], form["order_id"]):
                return render_template(
                    "order_page.html",
                    item=form["item"],
                    session_id=form["order_id"],
                    deleted=True,
                )
            else:
                return order_process("Not in basket")
        else:
            return order_process("Not all required filled")
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


@app.route("/submit", methods=["POST"])
@http_duration_metric.time()
def submit_order():
    form = request.form
    try:
        order_web_interface.submit_order(
            form["name"], form["address"], form["order_id"]
        )
        return render_template(
            "order_page.html", session_id=form["order_id"], session_submitted=True
        )
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


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
