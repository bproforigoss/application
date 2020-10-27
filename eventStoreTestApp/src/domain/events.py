import json
import uuid
import requests
from src import CONFIG


class Event:

    def __init__(self, event_type, aggregate_id, data):
        self.event_type = event_type
        self.aggregate_id = aggregate_id
        self.data = data

    def execute(self):
        es_id = uuid.uuid4()
        headers = {
            "Content-Type": "application/json",
            "ES-EventType": self.event_type.value,
            "ES-EventID": str(es_id)
        }
        request = requests.post(f"{CONFIG.EVENTSTORE_STREAM_URL}/{self.aggregate_id}",
                                data=json.dumps(self.data),
                                headers=headers)


class OrderEvent(Event):

    def __init__(self, event_type, order_aggregate_id, data):
        super().__init__(event_type, order_aggregate_id, data)


class StockEvent(Event):

    def __init__(self, event_type, product_stock_aggregate_id, data):
        super().__init__(event_type, product_stock_aggregate_id, data)
