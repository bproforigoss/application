import pytest
from order_service import app as microservice


@pytest.fixture
def app():
    yield microservice


@pytest.fixture
def client(app):
    return app.test_client()


def test_proper_html_on_first_index_request(client):
    res = client.get("/order")
    assert res.status_code == 200


def test_health_check(client):
    res = client.get("/order/health")
    assert res.status_code == 200
