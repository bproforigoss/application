import pytest
from inventory_service import app as microservice


@pytest.fixture
def app():
    yield microservice


@pytest.fixture
def client(app):
    return app.test_client()


def test_proper_html_on_first_index_request(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Item: Alma | Quantity: 20" not in res.data


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
