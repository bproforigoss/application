from inventory_service.domain import domain_events
from inventory_service.product_stock_aggregate import ProductStockAggregate
from inventory_service.domain.enumerations import ProductCatalogEventEnumeration as EVENT_TYPE

inventory = {}


def create_product(product_details):
    stock_id = product_details["name"]
    event = domain_events.StockEvent(EVENT_TYPE.ProductCreated, stock_id, product_details)
    event.execute()
    create_item_stock(product_details["name"], stock_id)


def create_item_stock(item, stock_id):
    if item not in inventory.keys():
        aggregate = ProductStockAggregate(item, 0)
        aggregate.aggregate_id = stock_id
        aggregate.create_stock("administratively created")
        inventory[item] = aggregate


def delete_product(product_name):
    if product_name in inventory.keys():
        event = domain_events.StockEvent(EVENT_TYPE.ProductDeleted, inventory[product_name].aggregate_id,
                                         {"reason": "administrative action"})
        event.execute()
        delete_item_stock(product_name)
        inventory.pop(product_name)


def delete_item_stock(item):
    for item_name in inventory.keys():
        if item_name == item:
            inventory[item].delete_stock("administratively deleted")
            return


def increase_item_amount(item, amount):
    if item in inventory.keys():
        inventory[item].add_stock(int(amount))


def decrease_item_amount(item, amount):
    if item in inventory.keys():
        inventory[item].subtract_stock(int(amount))
