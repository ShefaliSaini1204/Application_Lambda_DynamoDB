import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

def lambda_handler(event, context):
    http_method = event['httpMethod']

    # To create a new entry in table.
    if http_method == 'POST':
        student = json.loads(event['body'])
        table.put_item(Item=student)
        return {
            'statusCode': 200,
            'body': json.dumps('Student record added successfully')
        }

    # # To get details from table using student id.
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
                'body': json.dumps('Student details not found!!')
            }

    # To update the details in table.
    elif http_method == 'PUT':
        student = json.loads(event['body'])
        student_id = student['student_id']
      
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

    #To delete the details from the table.
    elif http_method == 'DELETE':
        student_id = event['queryStringParameters']['student_id']
        table.delete_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'body': json.dumps('Student record deleted successfully from the table!!')
        }

    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported HTTP method request.')
        }
    
