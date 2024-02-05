import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
from uuid import uuid4
import json
import re
from base64 import b64encode, b64decode
 
region_name = getenv('APP_REGION')
todos_persons_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePeople')
 
 
def lambda_handler(event, context):
    print(event)
    auth_header = event['headers']["Authorization"]
    allow = "Deny"
    
    matcher1 = re.match("^Basic (.+)$", auth_header)
    print(matcher1[1])
    
    credentials = b64decode(matcher1[1])
    print(credentials)
        
    # credentials is a byte string, so you have to use br in your regex
    matcher2 = re.match(br"^([^:]+):(.+)$", credentials)
        
    # coerce the bytes into an actual string you can use
    email = matcher2[1].decode('utf-8')
    password = matcher2[2].decode('utf-8')
        
    print(f'email: {email}, password: {password}')
 
    user_or_false = found_in_db(email, password)
 
    if user_or_false:
        print(f'user {email} found in db')
        allow = "Allow"
    else:
        print("user not found in db")
 
    
    response = {
        "principalId": f'{email}',
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": allow,
                    "Resource": event['methodArn']
                }
            ]
        },
        "context": {
            "email": email,
            "password": password,
            "userId": user_or_false["Id"],
            "role_name": user_or_false["role_name"]
        }
    }
    print(response)
    return response
 
def found_in_db(email, password):
    user = todos_persons_table.scan(FilterExpression=Attr('email').eq(email) & Attr('password').eq(password))

    if len(user["Items"]) == 1:
        return user["Items"][0]
    else:
        return False
 
"""
def found_in_db(email, password):
    output = todos_persons_table.get_item(Key={"Id":"3b9acad7-366a-46ae-b8e3-e0588ee73b49"})["Item"]
    print(output)
"""
 
 
 
# TEST JSON:
# {
#   "type": "TOKEN",
#   "authorizationToken": "authtoken99",
#   "methodArn": "arn:aws:execute-api:us-east-2:123456789012:example/prod/POST/{proxy+}",
#   "headers": {
#     "Authorization": "Basic Y2hyaXM6cHdkMTIz"
#   }
# }