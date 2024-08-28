import json
import boto3
import uuid

def add_user(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_table')

        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        password = body['password']

        new_user = {
            'userId': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'password': password,
        }

        table.put_item(Item=new_user)

        return {
            'statusCode': 201,
            'body': json.dumps(new_user)
        }

    except Exception as error:
        print(f"Error adding user: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to add user',
                'error': str(error)
            })

        }