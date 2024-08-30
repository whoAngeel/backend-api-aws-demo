import json
import boto3
import uuid
import hashlib
import os

def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password

def register_user(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_table')

        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        password = body['password']

        hashed_password = hash_password(password)

        new_user = {
            'userId': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'password': hashed_password.hex(),
        }

        table.put_item(Item=new_user)

        del new_user['password']

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