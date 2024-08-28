import json
import boto3

def get_task(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('task_table')

        userId = event['pathParameters']['userId']
        taskId = event['pathParameters']['taskId']

        get_result = table.get_item(
            Key={
                'userId': userId,
                'taskId': taskId
            }
        )
        task = get_result.get('Item')
        
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
