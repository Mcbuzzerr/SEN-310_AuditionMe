import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePeople')

def lambda_handler(event, context):
    person_id = str(uuid4())
    role_name = -1
    if ("/Director" == event["resource"]): 
        role_name = "Director"
    elif ("/Performer" == event["resource"]): 
        role_name = "Performer"
    
    body = json.loads(event["body"])
    name = body["name"]
    email = body["email"]
    phone = body["phone"]
    password = body["password"]
    past_performances = []
    planned_performances = []
    
    db_insert(person_id, name, email, phone, password, past_performances, planned_performances, role_name)
    return response(200, { "id": person_id })


    
def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body),
        "isBase64Encoded": False
    }

def db_insert(person_id, name, email, phone, password, past_performances, planned_performances, role_name):
 
    table.put_item(Item={
        'Id': person_id,
        'name' : name,
        'email' : email,
        'phone' : phone,
        'password' : password,
        'past_performances' : past_performances,
        'planned_performances' : planned_performances,
        'role_name' : role_name
    })