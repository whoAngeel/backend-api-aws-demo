import json
import boto3

def delete_task(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('task_table')

    userId = event['pathParameters']['userId']
    taskId = event['pathParameters']['taskId']

    try:
        # Obtener la tarea antes de eliminarla para verificar si existe
        get_result = table.get_item(
            Key={
                'userId': userId,
                'taskId': taskId
            }
        )

        task = get_result.get('Item')
        
        if not task:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }

        # Eliminar la tarea de DynamoDB
        table.delete_item(
            Key={
                'userId': userId,
                'taskId': taskId
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Task deleted successfully'})
        }

    except Exception as error:
        print(f"Error deleting task: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error deleting task',
                'error': str(error)
            })
        }
