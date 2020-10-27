from src.domain import events
from src.domain.aggregate import Aggregate
from src.domain.enumerations import InventoryEventEnumeration as INVENTORY_EVENT_TYPE
from src.domain.enumerations import ProductStockStatusEnumeration as PRODUCT_STOCK_STATUS


class ProductStockAggregate(Aggregate):

    def __init__(self, name, quantity):
        super().__init__()
        self.name = name
        self.quantity = quantity
        self.status = PRODUCT_STOCK_STATUS.INACTIVE

    def apply_event_effects_to_aggregate(self, event_json):
        event_type = event_json["summary"]
        data_dict = event_json["content"]["data"]

        if event_type is INVENTORY_EVENT_TYPE.StockCreated.value:
            self.status = PRODUCT_STOCK_STATUS.CREATED

        elif event_type is INVENTORY_EVENT_TYPE.StockAdded.value:
            self.quantity = data_dict["quantity"]

        elif event_type is INVENTORY_EVENT_TYPE.StockSubtracted.value:
            self.quantity = data_dict["quantity"]

        elif event_type is INVENTORY_EVENT_TYPE.StockDeleted.value:
            self.status = PRODUCT_STOCK_STATUS.DELETED

    def create_stock(self, reason):
        payload = {
            "reason": reason
        }
        self.raise_event(events.StockEvent(INVENTORY_EVENT_TYPE.StockCreated, self.aggregate_id, payload))
        self.version += 1
        self.status = PRODUCT_STOCK_STATUS.CREATED

    def delete_stock(self, reason):
        payload = {
            "reason": reason
        }
        self.raise_event(events.StockEvent(INVENTORY_EVENT_TYPE.StockDeleted, self.aggregate_id, payload))
        self.version += 1
        self.status = PRODUCT_STOCK_STATUS.DELETED

    def add_stock(self, quantity):
        self.quantity += quantity
        payload = {
            "quantity": str(self.quantity)
        }
        self.raise_event(events.StockEvent(INVENTORY_EVENT_TYPE.StockAdded, self.aggregate_id, payload))
        self.version += 1

    def subtract_stock(self, quantity):
        if self.quantity <= quantity:
            self.quantity -= quantity
            payload = {
                "quantity": str(self.quantity)
            }
            self.raise_event(events.StockEvent(INVENTORY_EVENT_TYPE.StockSubtracted, self.aggregate_id, payload))
            self.version += 1
