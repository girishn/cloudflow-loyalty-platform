# src/lambda/points-engine/lambda_function.py

import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
points_table = dynamodb.Table(os.environ['POINTS_TABLE'])
customers_table = dynamodb.Table(os.environ['CUSTOMERS_TABLE'])

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")
    
    http_method = event.get('httpMethod')
    path_parameters = event.get('pathParameters') or {}
    body = event.get('body')
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }
    
    try:
        if http_method == 'GET':
            customer_id = path_parameters.get('customerId')
            if customer_id:
                response = get_customer_points(customer_id)
            else:
                response = {'error': 'Customer ID is required'}
                
        elif http_method == 'POST':
            transaction_data = json.loads(body) if body else {}
            action = path_parameters.get('action', 'earn')
            
            if action == 'earn':
                response = earn_points(transaction_data)
            elif action == 'redeem':
                response = redeem_points(transaction_data)
            else:
                response = {'error': 'Invalid action'}
                
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

def get_customer_points(customer_id):
    try:
        # Get points history
        response = points_table.query(
            IndexName='CustomerIndex',
            KeyConditionExpression='customerId = :customerId',
            ExpressionAttributeValues={':customerId': customer_id},
            ScanIndexForward=False
        )
        
        # Get current total from customer table
        customer_response = customers_table.get_item(Key={'customerId': customer_id})
        if 'Item' not in customer_response:
            return {'statusCode': 404, 'error': 'Customer not found'}
        
        return {
            'customerId': customer_id,
            'totalPoints': customer_response['Item'].get('totalPoints', 0),
            'transactions': response.get('Items', [])
        }
        
    except Exception as e:
        raise Exception(f"Error getting points: {str(e)}")

def earn_points(transaction_data):
    try:
        customer_id = transaction_data['customerId']
        amount = Decimal(str(transaction_data['amount']))
        transaction_type = transaction_data.get('transactionType', 'purchase')
        
        # Calculate points based on transaction type
        points_earned = calculate_points(amount, transaction_type)
        
        transaction_id = f"{customer_id}#{int(datetime.utcnow().timestamp() * 1000)}"
        timestamp = datetime.utcnow().isoformat()
        
        # Create points transaction
        points_transaction = {
            'transactionId': transaction_id,
            'customerId': customer_id,
            'type': 'EARN',
            'points': points_earned,
            'amount': amount,
            'transactionType': transaction_type,
            'description': f"Earned {points_earned} points for {transaction_type}",
            'createdAt': timestamp
        }
        
        # Add to points table
        points_table.put_item(Item=points_transaction)
        
        # Update customer total points
        customers_table.update_item(
            Key={'customerId': customer_id},
            UpdateExpression='ADD totalPoints :points SET updatedAt = :timestamp',
            ExpressionAttributeValues={
                ':points': points_earned,
                ':timestamp': timestamp
            }
        )
        
        # Check for tier upgrade
        updated_customer = customers_table.get_item(Key={'customerId': customer_id})['Item']
        new_tier = calculate_tier(updated_customer['totalPoints'])
        
        if new_tier != updated_customer.get('tier'):
            customers_table.update_item(
                Key={'customerId': customer_id},
                UpdateExpression='SET tier = :tier',
                ExpressionAttributeValues={':tier': new_tier}
            )
            points_transaction['tierUpgrade'] = new_tier
        
        return {
            'statusCode': 201,
            'transaction': points_transaction,
            'newBalance': updated_customer['totalPoints'] + points_earned
        }
        
    except KeyError as e:
        return {'statusCode': 400, 'error': f'Missing required field: {str(e)}'}
    except Exception as e:
        raise Exception(f"Error earning points: {str(e)}")

def redeem_points(transaction_data):
    try:
        customer_id = transaction_data['customerId']
        points_to_redeem = Decimal(str(transaction_data['points']))
        reward_id = transaction_data.get('rewardId')
        
        # Check customer has enough points
        customer = customers_table.get_item(Key={'customerId': customer_id})['Item']
        if customer['totalPoints'] < points_to_redeem:
            return {'statusCode': 400, 'error': 'Insufficient points'}
        
        transaction_id = f"{customer_id}#{int(datetime.utcnow().timestamp() * 1000)}"
        timestamp = datetime.utcnow().isoformat()
        
        # Create points transaction
        points_transaction = {
            'transactionId': transaction_id,
            'customerId': customer_id,
            'type': 'REDEEM',
            'points': -points_to_redeem,
            'rewardId': reward_id,
            'description': f"Redeemed {points_to_redeem} points",
            'createdAt': timestamp
        }
        
        # Add to points table
        points_table.put_item(Item=points_transaction)
        
        # Update customer total points
        customers_table.update_item(
            Key={'customerId': customer_id},
            UpdateExpression='ADD totalPoints :points SET updatedAt = :timestamp',
            ExpressionAttributeValues={
                ':points': -points_to_redeem,
                ':timestamp': timestamp
            }
        )
        
        new_balance = customer['totalPoints'] - points_to_redeem
        
        return {
            'statusCode': 201,
            'transaction': points_transaction,
            'newBalance': new_balance
        }
        
    except KeyError as e:
        return {'statusCode': 400, 'error': f'Missing required field: {str(e)}'}
    except Exception as e:
        raise Exception(f"Error redeeming points: {str(e)}")

def calculate_points(amount, transaction_type):
    # Points calculation rules
    multipliers = {
        'purchase': Decimal('1'),
        'review': Decimal('50'),
        'referral': Decimal('100'),
        'bonus': Decimal('1')
    }
    
    multiplier = multipliers.get(transaction_type, Decimal('1'))
    
    if transaction_type in ['review', 'referral']:
        return multiplier  # Fixed points for these actions
    else:
        return int(amount * multiplier)  # Points per dollar spent

def calculate_tier(total_points):
    if total_points >= 10000:
        return 'Platinum'
    elif total_points >= 5000:
        return 'Gold'
    elif total_points >= 1000:
        return 'Silver'
    else:
        return 'Bronze'

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)