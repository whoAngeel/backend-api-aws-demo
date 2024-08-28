import json
import boto3

def get_users(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_table')

        response = table.scan()
        users = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(users)
        }

    except Exception as error:
        print(f"Error retrieving users: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve users',
                'error': str(error)
            })
        }