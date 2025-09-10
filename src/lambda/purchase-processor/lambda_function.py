import json
import boto3
import csv
import io
import os
from datetime import datetime
from decimal import Decimal
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Process purchase data files uploaded to S3 and call points engine
    """
    
    processed_records = 0
    failed_records = 0
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Only process purchase data files
        if not key.startswith('purchase-data/'):
            continue
            
        try:
            # Download and process file
            response = s3.get_object(Bucket=bucket, Key=key)
            file_content = response['Body'].read().decode('utf-8')
            
            # Process CSV data
            csv_reader = csv.DictReader(io.StringIO(file_content))
            
            for row in csv_reader:
                try:
                    # Validate required fields
                    if not all(field in row for field in ['customer_id', 'amount', 'timestamp']):
                        logger.warning(f"Missing required fields in row: {row}")
                        failed_records += 1
                        continue
                    
                    # Transform to match your earn_points format
                    transaction_data = {
                        'customerId': row['customer_id'],
                        'amount': float(row['amount']),
                        'transactionType': row.get('category', 'purchase').lower()
                    }
                    
                    # Call points engine directly
                    result = call_points_engine(transaction_data)
                    
                    if result.get('statusCode') == 201:
                        processed_records += 1
                        logger.info(f"Processed transaction for customer {row['customer_id']}")
                    else:
                        failed_records += 1
                        logger.error(f"Failed to process transaction: {result}")
                    
                except Exception as e:
                    logger.error(f"Failed to process row {row}: {str(e)}")
                    failed_records += 1
            
            # Move processed file to archive
            archive_key = key.replace('purchase-data/', 'purchase-data/processed/')
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=archive_key
            )
            s3.delete_object(Bucket=bucket, Key=key)
            
            logger.info(f"Processed file {key}: {processed_records} success, {failed_records} failed")
            
        except Exception as e:
            logger.error(f"Failed to process file {key}: {str(e)}")
            # Move to error folder
            error_key = key.replace('purchase-data/', 'purchase-data/error/')
            s3.copy_object(
                Bucket=bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=error_key
            )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed': processed_records,
            'failed': failed_records
        })
    }

def call_points_engine(transaction_data):
    """
    Call the points engine Lambda function to earn points
    """
    try:
        response = lambda_client.invoke(
            FunctionName=os.environ['POINTS_ENGINE_FUNCTION'],
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'httpMethod': 'POST',
                'path': '/earn',
                'body': json.dumps(transaction_data)
            })
        )
        
        result = json.loads(response['Payload'].read())
        return json.loads(result.get('body', '{}')) if 'body' in result else result
        
    except Exception as e:
        logger.error(f"Failed to call points engine: {str(e)}")
        return {'statusCode': 500, 'error': str(e)}
