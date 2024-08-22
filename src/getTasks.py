import json
import boto3

def get_tasks_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('TaskTable')

        response = table.scan()
        tasks = response.get('Items', [])

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
