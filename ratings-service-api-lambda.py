import boto3
import json
import os

print('Loading function')

ratings_dynamo_table_name = os.environ['ratings_dynamo_table_name']
ratings_dynamo_pkey = os.environ['ratings_dynamo_pkey']
ratings_dynamo_skey = os.environ['ratings_dynamo_skey']

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(Key=
            {
                ratings_dynamo_pkey : x[ratings_dynamo_pkey],
                ratings_dynamo_skey : x[ratings_dynamo_skey]
            }),
        'GET': lambda dynamo, x: dynamo.scan(Item=x),
        'POST': lambda dynamo, x: dynamo.put_item(Item=x),
        'PUT': lambda dynamo, x: dynamo.update_item(Item=x),
    }

    operation = event['httpMethod']
    print ('{} Lambda Event Handler: spoon-feed-ratings-service API handler'.format(operation))
    if operation in operations:
        print(event['body'])
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        dynamo = boto3.resource('dynamodb').Table(ratings_dynamo_table_name)
        rating = {}
        rating['user-id'] = payload['user-id']
        rating['restaurant-id'] = payload['restaurant']['restaurant-id']
        rating['rating-value'] = payload['rating-value']
        response = operations[operation](dynamo, rating)
        print ('Returning the following response: {}'.format(response))
        return respond(None, response)

    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
