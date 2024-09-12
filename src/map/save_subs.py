import json
import boto3
import uuid
from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def save_subs(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('map_table')

        body = json.loads(event['body'])
        name = body['name']
        coordinates = body['coordinates']

        latitude = Decimal(str(coordinates[0]))
        longitude = Decimal(str(coordinates[1]))

        new_subsidiary = {
            'subsId': str(uuid.uuid4()),
            'name': name,
            'geojson': {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude]
                },
                'properties': {
                    'name': name
                }
            }
        }

        table.put_item(Item=new_subsidiary)

        return {
            'statusCode': 201,
            'body': json.dumps(new_subsidiary, default = decimal_default)
        }
    
    except Exception as error:
        print(f"Error adding subsidiary: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to add subsidiary',
                'error': str(error)
            })
        }