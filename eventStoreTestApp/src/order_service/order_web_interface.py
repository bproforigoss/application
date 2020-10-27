from src.inventory_service import inventory_admin
from src.order_service import order_aggregate


def create_order_session():
    return order_aggregate.OrderAggregate()


def list_stock():
    available_stock = inventory_admin.inventory
    for item in available_stock.keys():
        print(f"{item.capitalize()} in stock. Amount: {available_stock[item].quantity}")


def add_item(item, amount, session):
    session.add_order_item(item, amount)


def remove_item(item, session):
    session.remove_order_item(item)


def submit_order(name, address, session):
    session.submit_order(name, address)
