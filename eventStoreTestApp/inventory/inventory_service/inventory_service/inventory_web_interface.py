from inventory_service.domain import domain_events
from inventory_service.domain.enumerations import (
    ProductCatalogEventEnumeration as EVENT_TYPE,
)
from inventory_service.product_stock_aggregate import ProductStockAggregate


inventory = {}


def create_product(product_details):
    stock_id = product_details["name"]
    if stock_id not in inventory.keys():
        event = domain_events.StockEvent(
            EVENT_TYPE.ProductCreated, stock_id, product_details
        )
        event.execute()
        create_item_stock(product_details["name"], stock_id)
    else:
        raise Exception("Item already in stock.")


def create_item_stock(item, stock_id):
    aggregate = ProductStockAggregate(item, 0)
    aggregate.aggregate_id = stock_id
    aggregate.create_stock("administratively created")
    inventory[item] = aggregate


def delete_product(product_name):
    if product_name in inventory.keys():
        event = domain_events.StockEvent(
            EVENT_TYPE.ProductDeleted,
            inventory[product_name].aggregate_id,
            {"reason": "administrative action"},
        )
        event.execute()
        delete_item_stock(product_name)
        inventory.pop(product_name)
    else:
        raise Exception("Item not in stock")


def delete_item_stock(item):
    for item_name in inventory.keys():
        if item_name == item:
            inventory[item].delete_stock("administratively deleted")
            return


def increase_item_amount(item, amount):
    if item in inventory.keys():
        inventory[item].add_stock(int(amount))
    else:
        raise Exception("Item not in stock")


def decrease_item_amount(item, amount):
    if item in inventory.keys():
        if inventory[item].amount <= amount:
            inventory[item].subtract_stock(int(amount))
        else:
            raise Exception("Current amount is lower than the subtracted amount")
    else:
        raise Exception("Item not in stock")
