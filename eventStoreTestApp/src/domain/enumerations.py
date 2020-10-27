from enum import Enum


class OrderStatusEnumeration(Enum):
    STARTED, SUBMITTED, ACCEPTED, REJECTED, DELETED = range(5)


class ProductStockStatusEnumeration(Enum):
    CREATED, DELETED, INACTIVE = range(3)


class OrderEventEnumeration(Enum):
    OrderItemAdded = "OrderItemAddedEvent"
    OrderItemRemoved = "OrderItemRemovedEvent"
    OrderStarted = "OrderStartedEvent"
    OrderSubmitted = "OrderSubmittedEvent"
    OrderDeleted = "OrderDeletedEvent"
    OrderAccepted = "OrderAcceptedEvent"
    OrderRejected = "OrderRejectedEvent"


class ProductCatalogEventEnumeration(Enum):
    ProductCreated = "ProductCreatedEvent"
    ProductDeleted = "ProductDeletedEvent"


class InventoryEventEnumeration(Enum):
    StockCreated = "StockCreatedEvent"
    StockDeleted = "StockDeletedEvent"
    StockAdded = "StockAddedEvent"
    StockSubtracted = "StockSubtractedEvent"
