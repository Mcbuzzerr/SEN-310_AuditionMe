import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
from uuid import uuid4
import json
from datetime import datetime

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePeople')

def lambda_handler(event, context):
    resource = event["resource"]
    resource = resource.split("/")[1]

    path = event["pathParameters"]
    id = path["id"]

    if "all" == id:
        output = table.scan()["Items"]
        for item in output:
            del item["password"]
            if item["role_name"] != resource:
                output.remove(item)
        
        return response(200, {
            "resource": resource,
            "data": output
        })


    output = table.get_item(Key={"Id":id})["Item"]

    if output is None:
        return response(404, "Person not found")

    del output["password"]
    if output["role_name"] != resource:
        return response(403, {"message": f"You are not authorized to access {output["role_name"]}"})
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