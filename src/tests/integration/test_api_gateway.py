# tests/integration/test_api_gateway.py
import requests
import pytest
import boto3

class TestAPIGateway:
    @pytest.fixture(scope="class")
    def api_url(self):
        return "https://your-api-id.execute-api.us-east-1.amazonaws.com/dev"
    
    def test_create_customer_endpoint(self, api_url):
        payload = {
            "email": "integration@test.com",
            "name": "Integration Test",
            "tier": "Bronze"
        }
        
        response = requests.post(f"{api_url}/customers", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data['email'] == payload['email']
        assert 'customer_id' in data
        
    def test_points_calculation(self, api_url):
        # Create customer first
        customer_response = requests.post(f"{api_url}/customers", json={
            "email": "points@test.com",
            "name": "Points Test"
        })
        customer_id = customer_response.json()['customer_id']
        
        # Add points transaction
        points_response = requests.post(f"{api_url}/points/earn", json={
            "customer_id": customer_id,
            "amount": 100,
            "transaction_type": "purchase"
        })
        
        assert points_response.status_code == 200
        assert points_response.json()['points_earned'] == 100