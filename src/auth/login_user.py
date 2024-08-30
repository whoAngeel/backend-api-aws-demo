import json
import boto3
import hashlib
import os
from boto3.dynamodb.conditions import Key

def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed_password

def validate_password(password, hashed_password):
    salt = hashed_password[:16]
    stored_hash = hashed_password[16:]
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return hashed_password == stored_hash

def login_user(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_table')

        body = json.loads(event['body'])
        email = body['email']
        password = body['password']

        response = table.query(
            IndexName = 'email-index',
            KeyConditionExpression = Key('email').eq(email)
        )

        if 'Items' not in response or len(response['Items']) == 0:
            return{
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }

        user = response['Items'][0]

        stored_password = bytes.fromhex(user['password'])

        if validate_password(stored_password, password):
            del user['password']
            return {
                'statusCode': 200,
                'body': json.dumps(user)
            }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid password'})
            }

    except Exception as error:
        print(f"Error validating user: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to validate user',
                'error': str(error)
            })
        }