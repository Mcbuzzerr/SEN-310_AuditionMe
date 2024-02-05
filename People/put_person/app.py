import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePeople')

def lambda_handler(event, context):
    # we just want to pass simple json and not use aws api lambda proxy integration, which is what we do normally on our own
    # however, when deploying as SAM app - this function receives the proxy integration automatically, so i have to check for it and fool it if it does
    #AWS PROXY REQUEST
    if ( ("body" in event) ):
        body = json.loads(event["body"])

    id = event['pathParameters']['id']
    name = body['name']
    email = body['email']
    password = body['password']
    phone = body["phone"]
    past_performances = body["past_performances"]
    planned_performances = body["planned_performances"]
    role_name = body["role_name"]

    
    if "id" is not event or id is None:
        response(400, "Id is required")

    person = table.get_item(Key={"Id":id})["Item"]
    
    if person is None:
        response(404, "Person not found")
    
    if name is not None:
        person['name'] = name
        
    if email is not None:
        person['email'] = email
        
    if password is not None:
        person['password'] = password

    if phone is not None:
        person['phone'] = phone
    
    if past_performances is not None:
        person['past_performances'] = past_performances

    if planned_performances is not None:
        person['planned_performances'] = planned_performances

    if role_name is not None:
        person['role_name'] = role_name


    table.put_item(Item=person)
    return response(200, person)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }