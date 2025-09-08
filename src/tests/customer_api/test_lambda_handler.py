import json
import pytest
from customer_api.lambda_function import lambda_handler

def test_get_customer_success(monkeypatch):
    event = {
        "httpMethod": "GET",
        "pathParameters": {"customerId": "123"},
        "body": None
    }

    def mock_get_customer(customer_id):
        return {"customer": {"customerId": customer_id, "name": "Test"}}

    monkeypatch.setattr("customer_api.lambda_function.get_customer", mock_get_customer)

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["customer"]["customerId"] == "123"


def test_get_all_customers_success(monkeypatch):
    event = {
        "httpMethod": "GET",
        "pathParameters": None,
        "body": None
    }

    def mock_get_all_customers():
        return {"customers": [{"customerId": "123", "name": "Test"}]}

    monkeypatch.setattr("customer_api.lambda_function.get_all_customers", mock_get_all_customers)

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert len(body["customers"]) == 1