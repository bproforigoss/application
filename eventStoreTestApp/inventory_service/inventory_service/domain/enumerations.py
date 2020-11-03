from enum import Enum


class ProductStockStatusEnumeration(Enum):
    CREATED, DELETED, INACTIVE = range(3)


class ProductCatalogEventEnumeration(Enum):
    ProductCreated = "ProductCreatedEvent"
    ProductDeleted = "ProductDeletedEvent"


class InventoryEventEnumeration(Enum):
    StockCreated = "StockCreatedEvent"
    StockDeleted = "StockDeletedEvent"
    StockAdded = "StockAddedEvent"
    StockSubtracted = "StockSubtractedEvent"
