from enum import Enum


class OrderStatusEnumeration(Enum):
    STARTED, SUBMITTED, ACCEPTED, REJECTED, DELETED = range(5)


class OrderEventEnumeration(Enum):
    OrderItemAdded = "OrderItemAddedEvent"
    OrderItemRemoved = "OrderItemRemovedEvent"
    OrderStarted = "OrderStartedEvent"
    OrderSubmitted = "OrderSubmittedEvent"
    OrderDeleted = "OrderDeletedEvent"
    OrderAccepted = "OrderAcceptedEvent"
    OrderRejected = "OrderRejectedEvent"
