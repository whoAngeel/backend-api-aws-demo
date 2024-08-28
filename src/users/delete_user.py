import json
import boto3

def delete_user(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_table')

    userId = event['pathParameters']['userId']

    try:
        get_result = table.get_item(Key={'userId': userId})
        if not get_result.get('Item'):
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }

        table.delete_item(Key={'userId': userId})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    
    except Exception as error:
        print(f"Error deleting user: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error deleting user',
                'error': str(error)
            })
        }