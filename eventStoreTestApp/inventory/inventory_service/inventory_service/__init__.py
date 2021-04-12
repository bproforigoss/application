import logging
import sys

from flask import Flask


logging.basicConfig(
    stream=sys.stdout,
    format='app=inventory_service where=%(filename)s level=%(levelname)s msg="%(message)s"',
    level=logging.INFO,
)

logging.info("app is being initialized")
app = Flask(__name__)


from inventory_service import views
