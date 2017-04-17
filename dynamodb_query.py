import boto3
import sys
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

if __name__ == "__main__":
    sum = 0
    type_req = sys.argv[1]
    year_req = sys.argv[2]
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('inf551_hw4')
    response = table.scan(
            FilterExpression=Attr('year').eq(year_req) & Attr('type').eq(type_req)
        )
    '''
    response2 = table.get_item(
        Key =  {
            'id' : 5
        }

    )
    '''
    items = response['Items']
    #items2 = response2['Item']
    #print 're2', response2
    #print 'items2', items2
    for item in items:
        #print "item",item
        sum += item.get('passenger_count')

    print(sum)

