#http://boto3.readthedocs.io/en/latest/guide/dynamodb.html
import boto3
import json
import sys

if __name__ == "__main__":
    json_file = sys.argv[1]
    json_data = json.load(open(json_file))['data']
    dynamodb = boto3.resource('dynamodb')
    #table = dynamodb.Table('inf551_hw4')
    table = dynamodb.create_table(
        TableName = 'inf551_hw4',
        KeySchema = [
            {
                'AttributeName':'id',
                'KeyType' : 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },


        ],

        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }

    )
    table.meta.client.get_waiter('table_exists').wait(TableName='inf551_hw4')
    print len(json_data)
    with table.batch_writer() as batch:
        count = 0
        for item in json_data:
            year = str(item[9]).split('-')[0]
            count += 1
            print int(item[13])
            batch.put_item(
                Item={
                    'id': item[0],
                    'year': year,
                    'type': item[11],
                    'passenger_count': int(item[13])
                }
            )
            if count == 1000:
                break
    
 








