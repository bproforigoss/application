import json
import os
import uuid

import requests

from .. import prom_logs


class Event:

    event_counter_metric = prom_logs.performance_metrics["event_send_counter"]
    network_error_metric = prom_logs.performance_metrics["network_error_counter"]
    http_error_metric = prom_logs.performance_metrics["http_error_counter"]
    timeout_error_metric = prom_logs.performance_metrics["timeout_error_counter"]
    redirect_error_metric = prom_logs.performance_metrics["redirect_error_counter"]

    def __init__(self, event_type, aggregate_id, data):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data

    @network_error_metric.count_exceptions(requests.exceptions.ConnectionError)
    @http_error_metric.count_exceptions(requests.exceptions.HTTPError)
    @timeout_error_metric.count_exceptions(requests.exceptions.Timeout)
    @redirect_error_metric.count_exceptions(requests.exceptions.TooManyRedirects)
    def execute(self):
        Event.event_counter_metric.inc()
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
            timeout=0.0000000002,
        )


class OrderEvent(Event):
    def __init__(self, event_type, order_aggregate_id, data):
        super().__init__(event_type, order_aggregate_id, data)
