import logging
import os
import sys

import prometheus_client
import requests
from flask import render_template, request, Response

from order_service import order_web_interface, app
from . import prom_logs

expected_main_error_types = [
    requests.exceptions.ConnectTimeout,
    requests.exceptions.HTTPError,
    requests.exceptions.ReadTimeout,
    requests.exceptions.TooManyRedirects,
    requests.exceptions.ConnectionError,
]
error_logging_messages = {
    "ConnectTimeout": f"network timeout error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "HTTPError": f"invalid HTTP response error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "ReadTimeout": f"communication timeout error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "TooManyRedirects": f"redirection error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "ConnectionError": f"connection error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "unknown error": f"ambiguous connection error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
}
error_logging_error_codes = {
    "ConnectTimeout": 502,
    "HTTPError": 502,
    "ReadTimeout": 504,
    "TooManyRedirects": 500,
    "ConnectionError": 500,
    "unknown error": 500,
}
error_logging_metrics = {
    "ConnectTimeout": prom_logs.performance_metrics["network_timeout_error_counter"],
    "HTTPError": prom_logs.performance_metrics["http_error_counter"],
    "ReadTimeout": prom_logs.performance_metrics["connection_timeout_error_counter"],
    "TooManyRedirects": prom_logs.performance_metrics["redirect_error_counter"],
    "ConnectionError": prom_logs.performance_metrics["connection_error_counter"],
    "unknown error": prom_logs.performance_metrics["ambiguous_network_error_counter"],
}

http_counter_metric = prom_logs.performance_metrics["http_request_counter"]


def log_and_return_connection_error_response(e):
    error_type = type(e)
    for expected_error_type in expected_main_error_types:
        if error_type is expected_error_type:
            error_logging_metrics[expected_error_type.__name__].inc()
            logging.error(
                f"{error_logging_messages[expected_error_type.__name__]} type {error_type.__name__}"
            )
            return Response(
                status=error_logging_error_codes[expected_error_type.__name__]
            )
    error_logging_metrics["unknown error"].inc()
    logging.error(
        f"{error_logging_messages['unknown error']} type {error_type.__name__}"
    )
    return Response(status=error_logging_error_codes["unknown error"])


@app.route("/", methods=["GET"])
def order_process(error=None):
    http_counter_metric.labels(method="GET", endpoint="/").inc()
    return render_template("order_page.html", error=error)


@app.route("/create", methods=["POST"])
def create_order_session():
    http_counter_metric.labels(method="POST", endpoint="/create").inc()
    try:
        created_id = order_web_interface.create_order_session()
        return render_template("order_created.html", id=created_id)
    except requests.exceptions.RequestException as e:
        return log_and_return_connection_error_response(e)
    except Exception as e:
        logging.error(f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}")
        return order_process(
            f"There was a problem in the operation of this software.\n{e}"
        )


@app.route("/add", methods=["POST"])
def add_to_order():
    http_counter_metric.labels(method="POST", endpoint="/add").inc()
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
    except requests.exceptions.RequestException as e:
        return log_and_return_connection_error_response(e)
    except Exception as e:
        logging.error(f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}")
        return order_process(
            f"There was a problem in the operation of this software.\n{e}"
        )


@app.route("/delete", methods=["POST"])
def delete_from_order():
    http_counter_metric.labels(method="POST", endpoint="/delete").inc()
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
    except requests.exceptions.RequestException as e:
        return log_and_return_connection_error_response(e)
    except Exception as e:
        logging.error(f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}")
        return order_process(
            f"There was a problem in the operation of this software.\n{e}"
        )


@app.route("/submit", methods=["POST"])
def submit_order():
    http_counter_metric.labels(method="POST", endpoint="/submit").inc()
    form = request.form
    try:
        order_web_interface.submit_order(
            form["name"], form["address"], form["order_id"]
        )
        return render_template(
            "order_page.html", session_id=form["order_id"], session_submitted=True
        )
    except requests.exceptions.RequestException as e:
        return log_and_return_connection_error_response(e)
    except Exception as e:
        logging.error(f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}")
        return order_process(
            f"There was a problem in the operation of this software.\n{e}"
        )


@app.route("/health", methods=["GET"])
def health_check():
    http_counter_metric.labels(method="GET", endpoint="/health").inc()
    return Response({"health check": "successful"}, status=200)


@app.route("/metrics", methods=["GET"])
def metrics():
    http_counter_metric.labels(method="GET", endpoint="/metrics").inc()
    readings = []
    for metric in prom_logs.performance_metrics.values():
        readings.append(prometheus_client.generate_latest(metric))
    readings.append(
        prometheus_client.generate_latest(prometheus_client.PROCESS_COLLECTOR)
    )
    return Response(readings, mimetype="text/plain")


logging.info("app has been configured successfully")
