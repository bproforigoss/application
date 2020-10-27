import uuid
from src.domain import events
from src.domain.enumerations import ProductCatalogEventEnumeration as EVENT_TYPE
from src.inventory_service import inventory_admin

catalog = {}


def create_product(product_details):
    stock_id = uuid.uuid4()
    event = events.StockEvent(EVENT_TYPE.ProductCreated, stock_id, product_details)
    event.execute()
    inventory_admin.create_item_stock(product_details["name"])
    catalog[product_details["name"]] = stock_id


def delete_product(product_name):
    if product_name in catalog.keys():
        event = events.StockEvent(EVENT_TYPE.ProductDeleted, catalog[product_name],
                                  {"reason": "administrative action"})
        event.execute()
        inventory_admin.delete_item_stock(product_name)
        catalog.pop(product_name)
