import json
import os
import uuid

import requests

from .. import prom_logs


class Event:

    events_sent_metric = prom_logs.performance_metrics["events_produced"]
    event_duration_metric = prom_logs.performance_metrics["event_send_duration"]

    def __init__(self, event_type, aggregate_id, data):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data

    @event_duration_metric.time()
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
        Event.events_sent_metric.inc()


class StockEvent(Event):
    def __init__(self, event_type, product_stock_aggregate_id, data):
        super().__init__(event_type, product_stock_aggregate_id, data)
