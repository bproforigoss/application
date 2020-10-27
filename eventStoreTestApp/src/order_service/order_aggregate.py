import uuid
from src.domain import events
from src.domain.aggregate import Aggregate
from src.domain.enumerations import OrderStatusEnumeration as ORDER_STATUS
from src.domain.enumerations import OrderEventEnumeration as ORDER_EVENT_TYPE


class OrderAggregate(Aggregate):

    def __init__(self):
        super().__init__()
        self.order_id = uuid.uuid4()
        self.order_items = {}
        self.customer_id = {}
        self.status = ORDER_STATUS.STARTED
        self.raise_event(events.OrderEvent(ORDER_EVENT_TYPE.OrderStarted,
                                           self.aggregate_id,
                                           {"reason": "new session"}))

    def apply_event_effects_to_aggregate(self, event_json):
        event_type = event_json["summary"]
        data_dict = event_json["content"]["data"]

        if event_type == ORDER_EVENT_TYPE.OrderItemAdded.value:
            self.order_items[data_dict["item"]] = data_dict["quantity"]

        elif event_type == ORDER_EVENT_TYPE.OrderItemRemoved.value:
            self.order_items.pop(data_dict["item"])

        elif event_type == ORDER_EVENT_TYPE.OrderSubmitted.value:
            self.customer_id["name"] = data_dict["name"]
            self.customer_id["address"] = data_dict["address"]
            self.status = ORDER_STATUS.SUBMITTED

        elif event_type == ORDER_EVENT_TYPE.OrderDeleted.value:
            self.status = ORDER_STATUS.DELETED

        elif event_type == ORDER_EVENT_TYPE.OrderRejected.value:
            self.status = ORDER_STATUS.REJECTED

    def add_order_item(self, item, quantity):
        if item in self.order_items.keys():
            self.order_items[item] += quantity
        else:
            self.order_items[item] = quantity
        payload = {
            "item": item,
            "quantity": quantity
        }
        self.raise_event(events.OrderEvent(ORDER_EVENT_TYPE.OrderItemAdded, self.aggregate_id, payload))
        self.version += 1

    def remove_order_item(self, item):
        if item in self.order_items.keys():
            self.order_items.pop(item)
            payload = {
                "item": item,
            }
            self.raise_event(events.OrderEvent(ORDER_EVENT_TYPE.OrderItemRemoved, self.aggregate_id, payload))
            self.version += 1

    def submit_order(self, name, address):
        self.customer_id["name"] = name
        self.customer_id["address"] = address
        payload = self.customer_id
        self.raise_event(events.OrderEvent(ORDER_EVENT_TYPE.OrderSubmitted, self.aggregate_id, payload))
        self.version += 1
        self.status = ORDER_STATUS.SUBMITTED

    def delete_order(self):
        if self.status == ORDER_STATUS.ACCEPTED:
            payload = {
                "reason": "Customer submitted delete request"
            }
            self.raise_event(events.OrderEvent(ORDER_EVENT_TYPE.OrderDeleted, self.aggregate_id, payload))
            self.version += 1
            self.status = ORDER_STATUS.DELETED
        else:
            print("Order cannot be deleted, still in process!")
