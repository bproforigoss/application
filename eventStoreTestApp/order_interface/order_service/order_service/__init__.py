# pylint: skip-file
# flake8: noqa
from flask import Flask, render_template, request

app = Flask(__name__)

import order_service.order_web_interface


@app.route("/order", methods=["GET"])
def order_process(error=None):
    return render_template("order_page.html", error=error)


@app.route("/order/create", methods=["GET", "POST"])
def create_order_session_reroute():
    created_id = order_web_interface.create_order_session()
    return create_order_session(created_id)


@app.route("/order/create?<session_id>", methods=["POST"])
def create_order_session(session_id):
    return render_template("order_created.html", id=session_id)


@app.route("/order/add", methods=["GET", "POST"])
def add_to_order_reroute():
    form = request.form
    if form["order_id"] != "" and form["item"] != "" and form["amount"] != "":
        order_web_interface.add_item(form["item"], form["amount"], form["order_id"])
        return add_to_order(form["order_id"], form["item"], form["amount"])
    else:
        return order_process("Not all required filled")


@app.route("/order/add?<session_id>&<item>&<amount>&<value>", methods=["POST"])
def add_to_order(session_id, item, amount):
    return render_template(
        "order_page.html", item=item, amount=amount, session_id=session_id, added=True
    )


@app.route("/order/delete", methods=["GET", "POST"])
def delete_from_order_reroute():
    form = request.form
    if form["order_id"] != "" and form["item"] != "":
        if order_web_interface.remove_item(form["item"], form["order_id"]):
            return delete_from_order(form["order_id"], form["item"])
        else:
            return order_process("Not in basket")
    else:
        return order_process("Not all required filled")


@app.route("/order/delete?<session_id>&<item>&<value>", methods=["POST"])
def delete_from_order(session_id, item):
    return render_template(
        "order_page.html", item=item, session_id=session_id, deleted=True
    )


@app.route("/order/submit", methods=["GET", "POST"])
def submit_order_reroute():
    form = request.form
    order_web_interface.submit_order(form["name"], form["address"], form["order_id"])
    return submit_order(form["order_id"])


@app.route("/order/submit?<session_id>", methods=["POST"])
def submit_order(session_id):
    return render_template(
        "order_page.html", session_id=session_id, session_submitted=True
    )
