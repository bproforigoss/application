import logging
import os
import sys

from flask import Flask


logging.basicConfig(
    stream=sys.stdout,
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.info(f"{os.getenv('FLASK_APP')} Flask app is being initialized")
app = Flask(__name__)


from inventory_service import views
