import json
import uuid
import requests


class OrderItemAdded:

    def __init__(self, order_aggregate, item, quantity):
        self.order_aggregate = order_aggregate
        self.item = item
        self.quantity = quantity

    def execute(self):
        es_id = uuid.uuid4()
        data = [
            {
              "item": self.item,
              "quantity": self.quantity
            }
        ]
        headers = {
            "Content-Type": "application/json",
            "ES-EventType": "OrderItemAddedEvent",
            "ES-EventID": str(es_id)
        }
        request = requests.post(f"http://127.0.0.1:2113/streams/{self.order_aggregate}",
                                data=json.dumps(data),
                                headers=headers)
        print(request)


class OrderItemRemoved:

    def __init__(self, order_aggregate, item):
        self.order_aggregate = order_aggregate
        self.item = item

    def execute(self):
        es_id = uuid.uuid4()
        data = [
            {
              "item": self.item,
            }
        ]
        headers = {
            "Content-Type": "application/json",
            "ES-EventType": "OrderItemRemovedEvent",
            "ES-EventID": str(es_id)
        }
        request = requests.post(f"http://127.0.0.1:2113/streams/{self.order_aggregate}",
                                data=json.dumps(data),
                                headers=headers)
        print(request)


class OrderSubmitted:

    def __init__(self, order_aggregate, name, address):
        self.order_aggregate = order_aggregate
        self.name = name
        self.address = address

    def execute(self):
        es_id = uuid.uuid4()
        data = [
            {
                "customer_name": self.name,
                "customer_address": self.address
            }
        ]
        headers = {
            "Content-Type": "application/json",
            "ES-EventType": "OrderSubmittedEvent",
            "ES-EventID": str(es_id)
        }
        request = requests.post(f"http://127.0.0.1:2113/streams/{self.order_aggregate}",
                                data=json.dumps(data),
                                headers=headers)
        print(request)
