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

    if "all" == path["id"]:
        return response(200, table.scan()["Items"])
    
    # if "mine" == path["id"]:
    #     if user_role == "Director":
    #         return response(200, 
    #             table.scan(FilterExpression=Attr("director").eq(event['requestContext']['authorizer']['userId'])
    #             | Attr("casting_director").eq(event['requestContext']['authorizer']['userId']))["Items"]
    #         )
    #     elif user_role == "Performer":
    #         return response(200, 
    #             table.scan(FilterExpression=Attr("cast").contains(event['requestContext']['authorizer']['userId'])
    #             | Attr("auditions").contains(event['requestContext']['authorizer']['userId']))["Items"]
    #         )

    if "open" == path["id"]:
        return response(200, table.scan(FilterExpression=Attr("status").eq("Open"))["Items"])

    id = path["id"]
    output = table.get_item(Key={"Id":id})["Item"]
    return response(200, output)
    

def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }