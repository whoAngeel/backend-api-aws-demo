import json
import boto3

def get_tasks(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('task_table')

        userId = event['pathParameters']['userId']

        response = table.query(
            KeyConditionExpression = boto3.dynamodb.conditions.Key('userId').eq(userId)
        )
        tasks = response.get('Items', [])

        tasks.sort(key=lambda x: x['createdAt'], reverse=True)

        return {
            'statusCode': 200,
            'body': json.dumps(tasks)
        }

    except Exception as error:
        print(f"Error retrieving tasks: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to retrieve tasks',
                'error': str(error)
            })
        }
