import boto3
import pytest
from moto import mock_dynamodb2
from customer_api.lambda_function import get_customer

@mock_dynamodb2
def test_get_customer_found():
    table_name = "Customers"
    dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "customerId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "customerId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
    )
    table.put_item(Item={"customerId": "123", "name": "Test User"})

    # Patch environment variable
    import os
    os.environ["CUSTOMERS_TABLE"] = table_name

    result = get_customer("123")
    assert result["customer"]["name"] == "Test User"
    assert result["statusCode"] == 200