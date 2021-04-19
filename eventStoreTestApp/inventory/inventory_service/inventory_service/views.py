import logging
import os
import sys

import prometheus_client
import requests
from flask import render_template, request, Response

from inventory_service import inventory_web_interface, app
from . import prom_logs

error_logging_messages = {
    "ConnectionError": f"network operation error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "HTTPError": f"invalid HTTP response error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "Timeout": f"timeout error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "TooManyRedirects": f"redirection error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
    "unknown error": f"ambiguous connection error while connecting to {os.getenv('EVENTSTORE_STREAM_URL')}",
}
error_logging_error_codes = {
    "ConnectionError": 502,
    "HTTPError": 502,
    "Timeout": 504,
    "TooManyRedirects": 500,
    "unknown error": 500,
}
http_counter_metric = prom_logs.performance_metrics["http_request_counter"]


@app.route("/", methods=["GET"])
def inventory_process(error=None):
    http_counter_metric.labels(method="GET", endpoint="/").inc()
    inventory = {
        item.name: item.amount for item in inventory_web_interface.inventory.values()
    }
    return render_template("inventory_page.html", inventory=inventory, error=error)


@app.route("/create", methods=["POST"])
def create_product():
    http_counter_metric.labels(method="POST", endpoint="/create").inc()
    name = request.form["name"]
    price = request.form["price"]
    currency = request.form["currency"]
    if name != "" and price != "" and currency != "":
        try:
            inventory_web_interface.create_product(
                {"name": name, "price": price, "currency": currency}
            )
        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            if error_type in error_logging_messages.keys():
                logging.error(f"{error_logging_messages[error_type]} type {error_type}")
                return Response(status=error_logging_error_codes[error_type])
            else:
                logging.error(f"{error_logging_messages['unknown error']} type {error_type}")
                return Response(status=error_logging_error_codes["unknown error"])
        except Exception as e:
            logging.error(
                f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}"
            )
            return inventory_process(
                f"There was a problem in the operation of this software.\n{e}"
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/delete", methods=["POST"])
def delete_product():
    http_counter_metric.labels(method="POST", endpoint="/delete").inc()
    name = request.form["namedelete"]
    if name != "":
        try:
            inventory_web_interface.delete_product(name)
        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            if error_type in error_logging_messages.keys():
                logging.error(f"{error_logging_messages[error_type]} type {error_type}")
                return Response(status=error_logging_error_codes[error_type])
            else:
                logging.error(f"{error_logging_messages['unknown error']} type {error_type}")
                return Response(status=error_logging_error_codes["unknown error"])
        except Exception as e:
            logging.error(
                f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}"
            )
            return inventory_process(
                f"There was a problem in the operation of this software.\n{e}"
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/add", methods=["POST"])
def add_stock():
    http_counter_metric.labels(method="POST", endpoint="/add").inc()
    name = request.form["nameaddsubtract"]
    amount = request.form["amountaddsubtract"]
    if name != "" and amount != "":
        try:
            inventory_web_interface.increase_item_amount(name, amount)
        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            if error_type in error_logging_messages.keys():
                logging.error(f"{error_logging_messages[error_type]} type {error_type}")
                return Response(status=error_logging_error_codes[error_type])
            else:
                logging.error(f"{error_logging_messages['unknown error']} type {error_type}")
                return Response(status=error_logging_error_codes["unknown error"])
        except Exception as e:
            logging.error(
                f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}"
            )
            return inventory_process(
                f"There was a problem in the operation of this software.\n{e}"
            )
        return inventory_process()
    return inventory_process("Not all required given!")


@app.route("/subtract", methods=["POST"])
def subtract_stock():
    http_counter_metric.labels(method="POST", endpoint="/subtract").inc()
    name = request.form["nameaddsubtract"]
    amount = request.form["amountaddsubtract"]
    if name != "" and amount != "":
        try:
            inventory_web_interface.decrease_item_amount(name, amount)
        except requests.exceptions.RequestException as e:
            error_type = type(e).__name__
            if error_type in error_logging_messages.keys():
                logging.error(f"{error_logging_messages[error_type]} type {error_type}")
                return Response(status=error_logging_error_codes[error_type])
            else:
                logging.error(f"{error_logging_messages['unknown error']} type {error_type}")
                return Response(status=error_logging_error_codes["unknown error"])
        except Exception as e:
            logging.error(
                f"{type(e).__name__} caught in {sys._getframe().f_code.co_name}"
            )
            return inventory_process(
                f"There was a problem in the operation of this software.\n{e}"
            )
        return inventory_process()
    return inventory_process("Not all required given!")


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
