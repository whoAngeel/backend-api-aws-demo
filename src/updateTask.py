import json
import boto3
from datetime import datetime

def updateTask_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TaskTable')

    id = event['pathParameters']['id']

    try:
        get_result = table.get_item(Key={'id': id})
        task = get_result.get('Item')

        if not task:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }

        # Actualizar 'completed' y 'updatedAt' 
        updatedat = datetime.now().isoformat()

        updated_result = table.update_item(
            Key={'id': id},
            UpdateExpression="SET completed = :newCompleted, updatedAt = :newUpdatedAt",
            ExpressionAttributeValues={
                ':newCompleted': not task['completed'],
                ':newUpdatedAt': updatedat
            },
            ReturnValues="ALL_NEW"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Task updated successfully',
                'task': updated_result['Attributes']
            })
        }

    except Exception as error:
        print(f"Error toggling task completion: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to update task',
                'error': str(error)
            })
        }
