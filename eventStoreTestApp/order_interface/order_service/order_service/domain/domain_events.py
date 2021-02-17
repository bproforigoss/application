import json
import os
import uuid

import requests

from .. import prom_logs


class Event:

    event_duration_metric = prom_logs.performance_metrics["event_send_summary"]
    error_metric = prom_logs.performance_metrics["connection_error_counter"]

    def __init__(self, event_type, aggregate_id, data):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data

    @event_duration_metric.time()
    @error_metric.count_exceptions()
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


class OrderEvent(Event):
    def __init__(self, event_type, order_aggregate_id, data):
        super().__init__(event_type, order_aggregate_id, data)
