import json
import boto3

def deleteTask_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TaskTable')

    id = event['pathParameters']['id']

    try:
        # Obtener la tarea antes de eliminarla para verificar si existe
        task_result = table.get_item(Key={'id': id})
        if not task_result.get('Item'):
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Task not found'})
            }

        # Eliminar la tarea de DynamoDB
        table.delete_item(Key={'id': id})

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
