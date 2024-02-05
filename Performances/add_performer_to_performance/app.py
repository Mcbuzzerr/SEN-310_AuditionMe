import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances')

def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST
    if ( ("body" in event) ):
        body = json.loads(event["body"])

    id = event['pathParameters']['id']
    auditions = None
    cast = None
    if "auditions" in body:
        auditions = body["auditions"]
    if "cast" in body:
        cast = body["cast"]
    

    
    if "id" not in event['pathParameters'] or event['pathParameters']['id'] == None:
        response(400, "Id is required")


    performance = table.get_item(Key={"Id":id})["Item"]

    
    if performance is None:
        response(404, "Performance not found")
    
    if auditions is not None:
        new_auditions = performance['auditions'] + auditions
        # Remove duplicates from the list
        performance['auditions'] = list(set(new_auditions))

    if cast is not None:
        new_cast = performance['cast'] + cast
        # Remove duplicates from the list
        performance['cast'] = list(set(new_cast))

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