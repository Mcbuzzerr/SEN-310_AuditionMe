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
        event = json.loads(event["body"])

    id = event['id']
    title = event["title"]
    director = event["director"]
    casting_director = event["casting_director"]
    performance_dates = event["performance_dates"]
    cast = event["cast"]
    venue = event["venue"]
    auditions = event["auditions"]
    status = event["status"]

    
    if "id" is not event or id is None:
        response(400, "Id is required")

    performance = table.get_item(Key={"Id":id})["Item"]
    
    if performance is None:
        response(404, "Person not found")
    
    if title is not None:
        performance['title'] = title
        
    if director is not None:
        performance['director'] = director

    if casting_director is not None:
        performance['casting_director'] = casting_director
        
    if performance_dates is not None:
        performance['performance_dates'] = performance_dates

    if cast is not None:
        performance['cast'] = cast
    
    if venue is not None:
        performance['venue'] = venue

    if auditions is not None:
        performance['auditions'] = auditions

    if status is not None:
        performance['status'] = status

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