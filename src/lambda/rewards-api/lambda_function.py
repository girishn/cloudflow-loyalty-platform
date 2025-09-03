# src/lambda/rewards-api/lambda_function.py

import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
rewards_table = dynamodb.Table(os.environ['REWARDS_TABLE'])
points_table = dynamodb.Table(os.environ['POINTS_TABLE'])

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
            reward_id = path_parameters.get('rewardId')
            if reward_id:
                response = get_reward(reward_id)
            else:
                response = get_all_rewards()
                
        elif http_method == 'POST':
            reward_data = json.loads(body) if body else {}
            response = create_reward(reward_data)
            
        elif http_method == 'PUT':
            reward_id = path_parameters.get('rewardId')
            if not reward_id:
                raise ValueError('Reward ID is required for update')
            update_data = json.loads(body) if body else {}
            response = update_reward(reward_id, update_data)
            
        elif http_method == 'DELETE':
            reward_id = path_parameters.get('rewardId')
            if not reward_id:
                raise ValueError('Reward ID is required for delete')
            response = delete_reward(reward_id)
            
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

def get_reward(reward_id):
    try:
        response = rewards_table.get_item(Key={'rewardId': reward_id})
        if 'Item' not in response:
            return {'statusCode': 404, 'error': 'Reward not found'}
        return {'reward': response['Item']}
    except Exception as e:
        raise Exception(f"Error getting reward: {str(e)}")

def get_all_rewards():
    try:
        # Get only active rewards by default
        response = rewards_table.scan(
            FilterExpression='#status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'Active'}
        )
        return {'rewards': response.get('Items', [])}
    except Exception as e:
        raise Exception(f"Error getting rewards: {str(e)}")

def create_reward(reward_data):
    try:
        reward_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        reward = {
            'rewardId': reward_id,
            'name': reward_data['name'],
            'description': reward_data.get('description', ''),
            'pointsCost': Decimal(str(reward_data['pointsCost'])),
            'category': reward_data.get('category', 'General'),
            'type': reward_data.get('type', 'Discount'),  # Discount, Product, Experience
            'value': reward_data.get('value'),  # Monetary value or percentage
            'termsConditions': reward_data.get('termsConditions', ''),
            'validFrom': reward_data.get('validFrom', timestamp),
            'validUntil': reward_data.get('validUntil'),
            'maxRedemptions': reward_data.get('maxRedemptions'),
            'currentRedemptions': Decimal('0'),
            'tierRestriction': reward_data.get('tierRestriction'),  # Bronze, Silver, Gold, Platinum
            'status': 'Active',
            'createdAt': timestamp,
            'updatedAt': timestamp
        }
        
        # Remove None values
        reward = {k: v for k, v in reward.items() if v is not None}
        
        rewards_table.put_item(Item=reward)
        
        return {'statusCode': 201, 'reward': reward}
        
    except KeyError as e:
        return {'statusCode': 400, 'error': f'Missing required field: {str(e)}'}
    except Exception as e:
        raise Exception(f"Error creating reward: {str(e)}")

def update_reward(reward_id, update_data):
    try:
        timestamp = datetime.utcnow().isoformat()
        
        # Build update expression
        update_expr = "SET updatedAt = :timestamp"
        expr_values = {':timestamp': timestamp}
        
        allowed_fields = [
            'name', 'description', 'pointsCost', 'category', 'type', 
            'value', 'termsConditions', 'validFrom', 'validUntil',
            'maxRedemptions', 'tierRestriction', 'status'
        ]
        
        for field in allowed_fields:
            if field in update_data:
                update_expr += f", {field} = :{field}"
                if field == 'pointsCost' and update_data[field] is not None:
                    expr_values[f':{field}'] = Decimal(str(update_data[field]))
                else:
                    expr_values[f':{field}'] = update_data[field]
        
        response = rewards_table.update_item(
            Key={'rewardId': reward_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ConditionExpression='attribute_exists(rewardId)',
            ReturnValues='ALL_NEW'
        )
        
        return {'reward': response['Attributes']}
        
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {'statusCode': 404, 'error': 'Reward not found'}
    except Exception as e:
        raise Exception(f"Error updating reward: {str(e)}")

def delete_reward(reward_id):
    try:
        # Soft delete by updating status
        timestamp = datetime.utcnow().isoformat()
        
        rewards_table.update_item(
            Key={'rewardId': reward_id},
            UpdateExpression='SET #status = :status, updatedAt = :timestamp',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'Inactive',
                ':timestamp': timestamp
            },
            ConditionExpression='attribute_exists(rewardId)'
        )
        
        return {'message': 'Reward deactivated successfully'}
        
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {'statusCode': 404, 'error': 'Reward not found'}
    except Exception as e:
        raise Exception(f"Error deleting reward: {str(e)}")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)