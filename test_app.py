import pytest
from flask import Flask
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


# def test_create_customer(client):
#     response = client.post("/customer")
#     # TODO: Add request body
#     assert response.status_code == 201


def test_get_customer(client):
    response = client.get("/customer/1234")
    assert response.status_code == 200


def test_delete_customer(client):
    response = client.delete("/customer/1234")
    assert response.status_code == 200
