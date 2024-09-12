import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_subs(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('map_table')

        name = event['pathParameters']['nameSubs']

        response = table.query(
            IndexName = 'name-index',
            KeyConditionExpression = Key('name').eq(name)
        )

        if 'Items' in response and len(response['Items']) > 0:
            subsidiary = response['Items'][0]

            return {
                'statusCode': 200,
                'body': json.dumps(subsidiary['geojson'], default=decimal_default)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Subsidiary not found'
                })
            }
    except Exception as error:
        print(f"Error retrieving subsidiary: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve subsidiary',
                'error': str(error)
        })
        }