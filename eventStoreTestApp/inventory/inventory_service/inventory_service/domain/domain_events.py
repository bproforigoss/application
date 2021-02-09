import json
import os
import uuid

import requests
from prometheus_client import Counter


class Event:

    event_metrics = {
        "events_produced": Counter("events_produced", "Events sent out by this microservice")
    }

    def __init__(self, event_type, aggregate_id, data):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data

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
        Event.event_metrics["events_produced"].inc()


class StockEvent(Event):
    def __init__(self, event_type, product_stock_aggregate_id, data):
        super().__init__(event_type, product_stock_aggregate_id, data)
