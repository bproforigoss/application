from inventory_service.domain import domain_events
from inventory_service.domain.aggregate import Aggregate
from inventory_service.domain.enumerations import (
    InventoryEventEnumeration as INVENTORY_EVENT_TYPE,
)
from inventory_service.domain.enumerations import (
    ProductStockStatusEnumeration as PRODUCT_STOCK_STATUS,
)


class ProductStockAggregate(Aggregate):
    def __init__(self, name, amount):
        super().__init__()
        self.name = name
        self.amount = amount
        self.status = PRODUCT_STOCK_STATUS.INACTIVE

    def apply_event_effects_to_aggregate(self, event_json):
        event_type = event_json["summary"]
        data_dict = event_json["content"]["data"]

        if event_type is INVENTORY_EVENT_TYPE.StockCreated.value:
            self.status = PRODUCT_STOCK_STATUS.CREATED

        elif event_type is INVENTORY_EVENT_TYPE.StockAdded.value:
            self.amount += data_dict["amount"]

        elif event_type is INVENTORY_EVENT_TYPE.StockSubtracted.value:
            self.amount -= data_dict["amount"]

        elif event_type is INVENTORY_EVENT_TYPE.StockDeleted.value:
            self.status = PRODUCT_STOCK_STATUS.DELETED

    def create_stock(self, reason):
        payload = {"reason": reason}
        self.raise_event(
            domain_events.StockEvent(
                INVENTORY_EVENT_TYPE.StockCreated, self.aggregate_id, payload
            )
        )
        self.version += 1
        self.status = PRODUCT_STOCK_STATUS.CREATED

    def delete_stock(self, reason):
        payload = {"reason": reason}
        self.raise_event(
            domain_events.StockEvent(
                INVENTORY_EVENT_TYPE.StockDeleted, self.aggregate_id, payload
            )
        )
        self.version += 1
        self.status = PRODUCT_STOCK_STATUS.DELETED

    def add_stock(self, quantity):
        payload = {"amount": str(quantity)}
        self.raise_event(
            domain_events.StockEvent(
                INVENTORY_EVENT_TYPE.StockAdded, self.aggregate_id, payload
            )
        )
        self.amount += quantity
        self.version += 1

    def subtract_stock(self, quantity):
        if self.amount >= quantity:
            payload = {"amount": str(quantity)}
            self.raise_event(
                domain_events.StockEvent(
                    INVENTORY_EVENT_TYPE.StockSubtracted, self.aggregate_id, payload
                )
            )
            self.amount -= quantity
            self.version += 1
