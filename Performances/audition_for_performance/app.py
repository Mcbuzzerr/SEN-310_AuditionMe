import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances')
person_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePeople')

def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST


    id = event['pathParameters']['id']

    performance = table.get_item(Key={"Id":id})["Item"]
    
    if performance is None:
        response(404, "Performance not found")
    if performance['status'] != "Open":
        response(400, "Performance is closed for auditions")
    
    performance['auditions'].append(event["requestContext"]["authorizer"]["userId"])
    person = person_table.get_item(Key={"Id":event["requestContext"]["authorizer"]["userId"]})["Item"]
    person['planned_performances'].append(id)
    person_table.put_item(Item=person)

    table.put_item(Item=performance)
    return response(200, performance)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }