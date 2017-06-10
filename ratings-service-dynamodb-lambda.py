import boto3
import json
import os

from neo4j.v1 import GraphDatabase, basic_auth

print('Loading function')

def lambda_handler(event, context):
    # Get the credentials for DB
    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=os.environ['secrets_s3_bucket'], Key=os.environ['db_secret_s3_key'])
    db_creds = json.load(s3_object['Body'])

    neo4j = GraphDatabase.driver(db_creds['connection'], auth=basic_auth(db_creds['username'], db_creds['password']))
    session = neo4j.session()

    for record in event['Records']:
        rating = record['dynamodb']['NewImage']
        print('Creating restaurant node in DB, restuarant-id: {}'.format(rating['restaurant-id']))
        session.run("CREATE (a:restaurant {id: {id}})",
              {'id': rating['restaurant-id']['S']})

    session.close()

    print('Successfully processed %s records.' % str(len(event['Records'])))
