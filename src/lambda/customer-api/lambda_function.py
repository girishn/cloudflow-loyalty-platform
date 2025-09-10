import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CUSTOMERS_TABLE'])

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    http_method = event.get('httpMethod')
    path_parameters = event.get('pathParameters') or {}
    body = event.get('body')
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
    }
    
    try:
        if http_method == 'GET':
            customer_id = path_parameters.get('customerId')
            if customer_id:
                response = get_customer(customer_id)
            else:
                response = get_all_customers()
                
        elif http_method == 'POST':
            customer_data = json.loads(body) if body else {}
            response = create_customer(customer_data)
            
        elif http_method == 'PUT':
            customer_id = path_parameters.get('customerId')
            if not customer_id:
                raise ValueError('Customer ID is required for update')
            update_data = json.loads(body) if body else {}
            response = update_customer(customer_id, update_data)
            
        elif http_method == 'DELETE':
            customer_id = path_parameters.get('customerId')
            if not customer_id:
                raise ValueError('Customer ID is required for delete')
            response = delete_customer(customer_id)
            
        else:
            raise ValueError(f'Unsupported method: {http_method}')
            
        return {
            'statusCode': response.get('statusCode', 200),
            'headers': headers,
            'body': json.dumps(response, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def get_customer(customer_id):
    try:
        response = table.get_item(Key={'customerId': customer_id})
        if 'Item' not in response:
            return {'statusCode': 404, 'error': 'Customer not found'}
        return {'customer': response['Item']}
    except Exception as e:
        raise Exception(f"Error getting customer: {str(e)}")

def get_all_customers():
    try:
        response = table.scan()
        return {'customers': response.get('Items', [])}
    except Exception as e:
        raise Exception(f"Error getting customers: {str(e)}")

def create_customer(customer_data):
    try:
        customer_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        customer = {
            'customerId': customer_id,
            'email': customer_data.get('email'),
            'firstName': customer_data.get('firstName'),
            'lastName': customer_data.get('lastName'),
            'phone': customer_data.get('phone'),
            'totalPoints': Decimal('0'),
            'tier': 'Bronze',
            'status': 'Active',
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Remove None values
        customer = {k: v for k, v in customer.items() if v is not None}
        
        table.put_item(
            Item=customer,
            ConditionExpression='attribute_not_exists(customerId)'
        )
        
        return {'statusCode': 201, 'customer': customer}
        
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {'statusCode': 409, 'error': 'Customer already exists'}
    except Exception as e:
        raise Exception(f"Error creating customer: {str(e)}")

def update_customer(customer_id, update_data):
    try:
        timestamp = datetime.utcnow().isoformat()
        
        # Build update expression
        update_expr = "SET updatedAt = :timestamp"
        expr_values = {':timestamp': timestamp}
        
        allowed_fields = ['email', 'firstName', 'lastName', 'phone', 'status']
        for field in allowed_fields:
            if field in update_data:
                update_expr += f", {field} = :{field}"
                expr_values[f':{field}'] = update_data[field]
        
        response = table.update_item(
            Key={'customerId': customer_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ConditionExpression='attribute_exists(customerId)',
            ReturnValues='ALL_NEW'
        )
        
        return {'customer': response['Attributes']}
        
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {'statusCode': 404, 'error': 'Customer not found'}
    except Exception as e:
        raise Exception(f"Error updating customer: {str(e)}")

def delete_customer(customer_id):
    try:
        table.delete_item(
            Key={'customerId': customer_id},
            ConditionExpression='attribute_exists(customerId)'
        )
        return {'message': 'Customer deleted successfully'}
        
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {'statusCode': 404, 'error': 'Customer not found'}
    except Exception as e:
        raise Exception(f"Error deleting customer: {str(e)}")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)