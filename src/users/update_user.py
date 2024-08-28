import json
import boto3

def update_user(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_table')

    userId = event['pathParameters']['userId']

    try:
        get_result = table.get_item(Key={'userId': userId})
        user = get_result.get('Item')

        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }
        
        body = json.loads(event['body'])
        name = body['name']

        updated_result = table.update_item(
            Key={'userId': userId},
            UpdateExpression="SET name = :newName",
            ExpressionAttributeValues={
                ':newName': name
            },
            ReturnValues="ALL_NEW"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'User updated successfully',
                'user': updated_result['Attributes']
            })
        }
    
    except Exception as error:
        print(f"Error updating user: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to update user',
                'error': str(error)
            })
        }