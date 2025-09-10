# Replace API_URL with API Gateway invoke URL

export API_URL="https://3mvwt3mo05.execute-api.us-east-1.amazonaws.com/dev"

# 1. Create a customer
curl -X POST $API_URL/customers \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
  }'

# 2. Get all customers
curl -X GET $API_URL/customers

# 3. Get specific customer (replace with actual customerId from step 1)
curl -X GET $API_URL/customers/{customerId}

# 4. Update customer
curl -X PUT $API_URL/customers/{customerId} \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "phone": "+0987654321"
  }'

# 5. Earn points for purchase
curl -X POST $API_URL/points/earn \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "{customerId}",
    "amount": 100.50,
    "transactionType": "purchase"
  }'

# 6. Earn points for review
curl -X POST $API_URL/points/earn \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "{customerId}",
    "amount": 0,
    "transactionType": "review"
  }'

# 7. Get customer points history
curl -X GET $API_URL/points/{customerId}

# 8. Create a reward
curl -X POST $API_URL/rewards \
  -H "Content-Type: application/json" \
  -d '{
    "name": "10% Off Coupon",
    "description": "Get 10% off your next purchase",
    "pointsCost": 500,
    "category": "Discount",
    "type": "Discount",
    "value": "10%",
    "termsConditions": "Valid for 30 days"
  }'

# 9. Get all rewards
curl -X GET $API_URL/rewards

# 10. Redeem points for reward
curl -X POST $API_URL/points/redeem \
  -H "Content-Type: application/json" \
  -d '{
    "customerId": "{customerId}",
    "points": 500,
    "rewardId": "{rewardId}"
  }'

# 11. Update reward status
curl -X PUT $API_URL/rewards/{rewardId} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Inactive"
  }'

# 12. Delete customer (soft delete)
curl -X DELETE $API_URL/customers/{customerId}