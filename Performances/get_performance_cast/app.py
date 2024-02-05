import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
from uuid import uuid4
import json
from datetime import datetime

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances')

def lambda_handler(event, context):
    path = event["pathParameters"]
    user_role = event['requestContext']['authorizer']['role_name']
    
    performances = []

    if "mine" == path["id"]:
        if user_role == "Director":
            performances.append(table.scan(FilterExpression=Attr("director").eq(event['requestContext']['authorizer']['userId'])["Items"] | Attr("casting_director").eq(event['requestContext']['authorizer']['userId'])["Items"]))
            
        elif user_role == "Performer":
            performances.append(table.scan(FilterExpression=Attr("cast").contains(event['requestContext']['authorizer']['userId'])["Items"]))
    else:
        id = path["id"]
        performances.append(table.get_item(Key={"Id":id})["Item"])


    for performance in performances:
        fetched_cast = []
        for audition in performance["cast"]:
            fetched_cast.append(boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePeople').get_item(Key={"Id":audition})["Item"])
        performance["cast"] = fetched_cast

    return response(200, performances)
    

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }