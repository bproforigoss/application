import json
import os
import uuid

import requests

from .. import prom_logs


class Event:

    event_summary_metric = prom_logs.performance_metrics["event_send_summary"]
    network_error_metric = prom_logs.performance_metrics["network_error_counter"]
    http_error_metric = prom_logs.performance_metrics["http_error_counter"]
    timeout_error_metric = prom_logs.performance_metrics["timeout_error_counter"]
    redirect_error_metric = prom_logs.performance_metrics["redirect_error_counter"]

    def __init__(self, event_type, aggregate_id, data):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data

    @event_summary_metric.time()
    @network_error_metric.count_exceptions(requests.exceptions.ConnectionError)
    @http_error_metric.count_exceptions(requests.exceptions.HTTPError)
    @timeout_error_metric.count_exceptions(requests.exceptions.Timeout)
    @redirect_error_metric.count_exceptions(requests.exceptions.TooManyRedirects)
    def execute(self):
        es_id = uuid.uuid4()
        headers = {
            "Content-Type": "application/json",
            "ES-EventType": self.event_type.value,
            "ES-EventID": str(es_id),
        }
        requests.post(
            f"{os.getenv('EVENTSTORE_STREAM_URL')}/{self.aggregate_id}",
            data=json.dumps(self.data),
            headers=headers,
        )


class StockEvent(Event):
    def __init__(self, event_type, product_stock_aggregate_id, data):
        super().__init__(event_type, product_stock_aggregate_id, data)
