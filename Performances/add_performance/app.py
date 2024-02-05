import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances')

def lambda_handler(event, context):
    body = json.loads(event["body"])

    performance_id = str(uuid4())    
    title = body["title"]
    director = body["director"]
    casting_director = body["casting_director"]
    performance_dates = body["performance_dates"]
    cast = body["cast"]
    venue = body["venue"]
    auditions = []
    status = "Open"
    
    db_insert(performance_id, title, director, casting_director, performance_dates, cast, venue, auditions, status)
    return response(200, { "id": performance_id })
    
def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }

def db_insert(performance_id, title, director, casting_director, performance_dates, cast, venue, auditions, status):
 
    table.put_item(Item={
        'Id': performance_id,
        'title' : title,
        'director' : director,
        'casting_director' : casting_director,
        'performance_dates' : performance_dates,
        'cast' : cast,
        'venue' : venue,
        'auditions' : auditions,
        'status' : status
    })