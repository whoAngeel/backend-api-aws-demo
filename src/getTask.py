import json
import boto3

def getTask_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('TaskTable')

        id = event['pathParameters']['id']

        response = table.get_item(Key={'id': id})
        task = response.get('Item')
        
        if task:
            return {
                'statusCode': 200,
                'body': json.dumps(task)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Task not found'
                })
            }

    except Exception as error:
        print(f"Error retrieving task: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve task',
                'error': str(error)
            })
        }
