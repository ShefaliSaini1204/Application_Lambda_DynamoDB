
import json
import boto3
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

def lambda_handler(event, context):
    http_method = event['httpMethod']

    # CREATE (POST)
    if http_method == 'POST':
        student = json.loads(event['body'])
        table.put_item(Item=student)
        return {
            'statusCode': 200,
            'body': json.dumps('Student record added successfully')
        }

    # READ (GET)
    elif http_method == 'GET':
        student_id = event['queryStringParameters']['student_id']
        response = table.get_item(Key={'student_id': student_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Student not found')
            }

    # UPDATE (PUT)
    elif http_method == 'PUT':
        student = json.loads(event['body'])
        student_id = student['student_id']
        # Example: update the "name" field
        response = table.update_item(
            Key={'student_id': student_id},
            UpdateExpression="set #n = :name",
            ExpressionAttributeNames={'#n': 'name'},
            ExpressionAttributeValues={':name': student['name']},
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student updated', 'updated': response['Attributes']})
        }

    # DELETE (DELETE)
    elif http_method == 'DELETE':
        student_id = event['queryStringParameters']['student_id']
        table.delete_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'body': json.dumps('Student record deleted successfully')
        }

    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported HTTP method')
        }
    