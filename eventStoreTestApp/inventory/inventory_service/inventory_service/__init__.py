from flask import Flask


app = Flask(__name__)


from inventory_service import views
