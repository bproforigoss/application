import uuid
import enum

import requests
import Events


class OrderStatusEnum(enum.Enum):
    STARTED, SUBMITTED, ACCEPTED, REJECTED, DELETED = range(5)


class Aggregate:

    def __init__(self):
        self.aggregate_id = uuid.uuid4()
        self.version = 0

    def raise_event(self, event_type):
        event_type.execute()

    def load_up(self):
        pass


class OrderAggregate(Aggregate):

    def __init__(self):
        super().__init__()
        self.order_id = uuid.uuid4()
        self.order_items = {}
        self.customer_id = {}
        self.status = OrderStatusEnum.STARTED

    def load_up(self):
        version = self.version
        while True:
            request = requests.get(f"http://127.0.0.1:2113/streams/{self.aggregate_id}/{version}",
                                   headers={"Accept": "application/vnd.eventstore.atom+json"})
            if request.status_code == 200:
                event_json = request.json()
                apply_event(event_json, self)
                event_type = event_json["summary"]
                print(f"Aggregate version {version}\nEvent: {event_type}State:\n{self}")
                version += 1
            else:
                return

    def add_order_item(self, item, quantity):
        if item in self.order_items.keys():
            self.order_items[item] += quantity
        else:
            self.order_items[item] = quantity
        self.raise_event(Events.OrderItemAdded(self.aggregate_id, item, quantity))
        self.version += 1

    def remove_order_item(self, item):
        if item in self.order_items.keys():
            self.order_items.pop(item)
            self.raise_event(Events.OrderItemRemoved(self.aggregate_id, item))
            self.version += 1

    def submit_order(self, name, address):
        self.customer_id["name"] = name
        self.customer_id["address"] = address
        self.raise_event(Events.OrderSubmitted(self.aggregate_id, name, address))
        self.version += 1
        self.status = OrderStatusEnum.SUBMITTED

    def delete_order(self):
        if self.status == OrderStatusEnum.ACCEPTED:
            self.raise_event(Events.OrderDeleted())
            self.version += 1
            self.status = OrderStatusEnum.DELETED
        else:
            print("Order cannot be deleted, still in process!")

    def __str__(self):
        return f"Items: {self.order_items}\nStatus: {self.status}\n"


def apply_event(event_json, aggregate_object):
    event_type = event_json["summary"]
    data_dict = event_json["content"]["data"][0]
    if event_type == "OrderItemAddedEvent":
        aggregate_object.order_items[data_dict["item"]] = data_dict["quantity"]
    elif event_type == "OrderItemRemovedEvent":
        aggregate_object.order_items.pop(data_dict["item"])
    elif event_type == "OrderSubmittedEvent":
        aggregate_object.status = OrderStatusEnum.SUBMITTED
