import prometheus_client
import requests
from flask import render_template, request, Response

from order_service import order_web_interface, app
from . import prom_logs


http_duration_metric = prom_logs.performance_metrics["http_request_summary"]


@app.route("/", methods=["GET"])
def order_process(error=None):
    return render_template("order_page.html", error=error)


@app.route("/create", methods=["GET", "POST"])
@http_duration_metric.time()
def create_order_session_reroute():
    try:
        created_id = order_web_interface.create_order_session()
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")
    return create_order_session(created_id)


@app.route("/create?<session_id>", methods=["POST"])
def create_order_session(session_id):
    return render_template("order_created.html", id=session_id)


@app.route("/add", methods=["GET", "POST"])
@http_duration_metric.time()
def add_to_order_reroute():
    form = request.form
    try:
        if form["order_id"] != "" and form["item"] != "" and form["amount"] != "":
            order_web_interface.add_item(form["item"], form["amount"], form["order_id"])
            return add_to_order(form["order_id"], form["item"], form["amount"])
        else:
            return order_process("Not all required filled")
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


@app.route("/add?<session_id>&<item>&<amount>&<value>", methods=["POST"])
def add_to_order(session_id, item, amount):
    return render_template(
        "order_page.html", item=item, amount=amount, session_id=session_id, added=True
    )


@app.route("/delete", methods=["GET", "POST"])
@http_duration_metric.time()
def delete_from_order_reroute():
    form = request.form
    try:
        if form["order_id"] != "" and form["item"] != "":
            if order_web_interface.remove_item(form["item"], form["order_id"]):
                return delete_from_order(form["order_id"], form["item"])
            else:
                return order_process("Not in basket")
        else:
            return order_process("Not all required filled")
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


@app.route("/delete?<session_id>&<item>&<value>", methods=["POST"])
def delete_from_order(session_id, item):
    return render_template(
        "order_page.html", item=item, session_id=session_id, deleted=True
    )


@app.route("/submit", methods=["GET", "POST"])
@http_duration_metric.time()
def submit_order_reroute():
    form = request.form
    try:
        order_web_interface.submit_order(
            form["name"], form["address"], form["order_id"]
        )
        return submit_order(form["order_id"])
    except requests.exceptions.RequestException:
        return order_process("There was a problem connecting to the database services.")


@app.route("/submit?<session_id>", methods=["POST"])
def submit_order(session_id):
    return render_template(
        "order_page.html", session_id=session_id, session_submitted=True
    )


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
