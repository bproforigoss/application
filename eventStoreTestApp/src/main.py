from src.inventory_service import inventory_admin, product_catalog_admin
from src.order_service import order_web_interface
from src.order_service.order_aggregate import OrderAggregate

product_catalog_admin.create_product({"name": "milk", "price": "1.5", "currency": "GBP"})
product_catalog_admin.create_product({"name": "bread", "price": "0.89", "currency": "GBP"})
product_catalog_admin.create_product({"name": "butter", "price": "1.15", "currency": "GBP"})

print(product_catalog_admin.catalog)

inventory_admin.increase_item_amount("milk", 50)
inventory_admin.increase_item_amount("bread", 30)
inventory_admin.increase_item_amount("butter", 10)

order_web_interface.list_stock()

session = order_web_interface.create_order_session()

order_web_interface.add_item("milk", 3, session)
order_web_interface.add_item("bread", 1, session)
order_web_interface.add_item("bread", 1, session)
order_web_interface.remove_item("milk", session)
order_web_interface.submit_order("KD", "Valahol", session)
print(f"{session.version}\n{session.status}\n{session.customer_id}\n{session.order_items}")

aggr = OrderAggregate()
aggr.aggregate_id = session.aggregate_id
aggr.load_up()
