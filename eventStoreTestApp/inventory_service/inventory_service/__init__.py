from flask import Flask, render_template, request

app = Flask(__name__)

import inventory_service.inventory_web_interface


@app.route('/inventory')
def inventory_process(error=None):
    inventory = {item.name: item.amount for item in inventory_web_interface.inventory.values()}
    return render_template('inventory_page.html', inventory=inventory, error=error)


@app.route('/inventory/create', methods=['GET', 'POST'])
def create_product_reroute():
    name = request.form["name"]
    price = request.form["price"]
    currency = request.form["currency"]
    if name != "" and price != "" and currency != "":
        return create_product(name, price, currency)
    return inventory_process("Not all required given!")


@app.route('/inventory/create?<name>&<price>&<currency>', methods=['POST'])
def create_product(name, price, currency):
    inventory_web_interface.create_product({"name": name,
                                            "price": price,
                                            "currency": currency})
    return inventory_process()


@app.route('/inventory/delete', methods=['GET', 'POST'])
def delete_product_reroute():
    name = request.form["namedelete"]
    if name != "":
        return delete_product(name)
    return inventory_process("Not all required given!")


@app.route('/inventory/delete?<name>', methods=['POST'])
def delete_product(name):
    inventory_web_interface.delete_product(name)
    return inventory_process()


@app.route('/inventory/add', methods=['GET', 'POST'])
def add_stock_reroute():
    name = request.form["nameaddsubtract"]
    amount = request.form["amountaddsubtract"]
    if name != "" and amount != "":
        return add_stock(name, amount)
    return inventory_process("Not all required given!")


@app.route('/inventory/add?<name>&<amount>', methods=['POST'])
def add_stock(name, amount):
    inventory_web_interface.increase_item_amount(name, amount)
    return inventory_process()


@app.route('/inventory/subtract', methods=['GET', 'POST'])
def subtract_stock_reroute():
    name = request.form["nameaddsubtract"]
    amount = request.form["amountaddsubtract"]
    if name != "" and amount != "":
        return subtract_stock(name, amount)
    return inventory_process("Not all required given!")


@app.route('/inventory/subtract?<name>&<amount>', methods=['POST'])
def subtract_stock(name, amount):
    inventory_web_interface.decrease_item_amount(name, amount)
    return inventory_process()
