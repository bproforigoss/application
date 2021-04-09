import logging
import os

from flask import Flask


logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.info(f"{os.getenv('FLASK_APP')} Flask app is being initialized")
app = Flask(__name__)


from inventory_service import views
