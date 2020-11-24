from flask import Flask

app = Flask(__name__)

from order_service import views
