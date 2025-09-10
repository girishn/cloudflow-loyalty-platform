import requests
import pytest

class TestLoyaltyWorkflow:
   def test_complete_customer_journey(self, api_url):
        # 1. Customer registration
        customer_data = {
            "email": "journey@test.com",
            "name": "Journey Test",
            "phone": "+1234567890"
        }
        customer_response = requests.post(f"{api_url}/customers/" + "{proxy+}", json=customer_data)
        assert customer_response.status_code == 201
        customer_id = customer_response.json().get("customer", {}).get("customerId")
        
        # 2. Make purchase and earn points
        purchase_data = {
            "customer_id": customer_id,
            "amount": 250,
            "transaction_type": "purchase"
        }
        points_response = requests.post(f"{api_url}/points/earn", json=purchase_data)
        assert points_response.status_code == 200
        
        # 3. Check customer points balance
        balance_response = requests.get(f"{api_url}/customers/{customer_id}/balance")
        assert balance_response.status_code == 200
        assert balance_response.json()['total_points'] == 250
        
        # 4. Redeem reward
        redemption_data = {
            "customer_id": customer_id,
            "reward_id": "discount_10_percent",
            "points_cost": 100
        }
        redemption_response = requests.post(f"{api_url}/rewards/redeem", json=redemption_data)
        assert redemption_response.status_code == 200
        
        # 5. Verify updated balance
        final_balance = requests.get(f"{api_url}/customers/{customer_id}/balance")
        assert final_balance.json()['total_points'] == 150