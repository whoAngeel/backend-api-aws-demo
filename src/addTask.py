import json
import boto3
import uuid

def add_task_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('TaskTable')

        body = json.loads(event['body'])
        title = body['title']

        created_at = updated_at = datetime.utcnow().isoformat()

        new_task = {
            'id': str(uuid.uuid4()),
            'title': title,
            'completed': False,
            'createdAt': created_at,
            'updatedAt': updated_at,
        }

        table.put_item(Item=new_task)

        return {
            'statusCode': 201,
            'body': json.dumps(new_task)
        }

    except Exception as error:
        print(f"Error adding task: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to add task',
                'error': str(error)
            })
        }
