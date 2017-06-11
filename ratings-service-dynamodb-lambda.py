import boto3
import json
import os

from neo4j.v1 import GraphDatabase, basic_auth

print('Loading function')

create_relationship_str = """MERGE (r:Restaurant {{restaurant_id: '{restaurant_id}'}})
    MERGE (u:User {{user_id: '{user_id}'}})
    MERGE (u)-[:{relationship}]-(r)"""

delete_relationship_str = """MATCH (u:User {{user_id: '{user_id}'}})-[k]-(r:Restaurant {{restaurant_id: '{restaurant_id}'}}) 
    DELETE k"""

relationship_map = { '0' : 'DISLIKES', '1' : 'LIKES'}

def lambda_handler(event, context):
    # Get the credentials for DB
    s3 = boto3.client('s3')
    s3_object = s3.get_object(Bucket=os.environ['secrets_s3_bucket'], Key=os.environ['db_secret_s3_key'])
    db_creds = json.load(s3_object['Body'])

    neo4j = GraphDatabase.driver(db_creds['connection'], auth=basic_auth(db_creds['username'], db_creds['password']))
    session = neo4j.session()

    for record in event['Records']:
        if 'NewImage' in record['dynamodb']:
            rating = record['dynamodb']['NewImage']
            user_id = rating['user-id']['S']
            restaurant_id = rating['restaurant-id']['S']
            rating_val = rating['rating-value']['N']
            relationship = relationship_map[rating_val]
            params = { 'restaurant_id' : restaurant_id, 'user_id' : user_id, 'relationship' : relationship }
            
            command = delete_relationship_str.format(**params)
            print('Deleting old relationship between {} & {} , restuarant-id'.format(user_id, restaurant_id))
            session.run(command)
            
            command = create_relationship_str.format(**params)
            print('Creating relationship {} - {} - {}'.format(user_id, relationship, restaurant_id))
            session.run(command)

    session.close()

    print('Successfully processed %s records.' % str(len(event['Records'])))
