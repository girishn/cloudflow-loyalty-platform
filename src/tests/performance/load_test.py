from locust import HttpUser, task, between

class LoyaltyFlowUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Create a test customer
        response = self.client.post("/customers", json={
            "email": f"loadtest{self.environment.parsed_options.locustfile}@test.com",
            "name": "Load Test User"
        })
        self.customer_id = response.json()['customer_id']
    
    @task(3)
    def get_customer_balance(self):
        self.client.get(f"/customers/{self.customer_id}/balance")
    
    @task(2)
    def earn_points(self):
        self.client.post("/points/earn", json={
            "customer_id": self.customer_id,
            "amount": 50,
            "transaction_type": "purchase"
        })
    
    @task(1)
    def view_rewards(self):
        self.client.get("/rewards")