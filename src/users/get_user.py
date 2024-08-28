import json
import boto3

def get_user(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_table')

        userId = event['pathParameters']['userId']

        get_result = table.get_item(Key={'userId': userId})
        user = get_result.get('Item')
        
        if user:
            return {
                'statusCode': 200,
                'body': json.dumps(user)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'User not found'
                })
            }
        
    except Exception as error:
        print(f"Error retrieving user: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve user',
                'error': str(error)
            })
        }