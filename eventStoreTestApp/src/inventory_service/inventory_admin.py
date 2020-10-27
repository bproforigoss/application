from src.inventory_service.product_stock_aggregate import ProductStockAggregate

inventory = {}


def create_item_stock(item):
    if item not in inventory.keys():
        aggregate = ProductStockAggregate(item, 0)
        aggregate.create_stock("administratively created")
        inventory[item] = aggregate


def delete_item_stock(item):
    for item_name in inventory.keys():
        if item_name == item:
            inventory[item].delete_stock("administratively deleted")
            return


def increase_item_amount(item, amount):
    if item in inventory.keys():
        inventory[item].add_stock(amount)


def decrease_item_amount(item, amount):
    if item in inventory.keys():
        inventory[item].subtract_stock(amount)
