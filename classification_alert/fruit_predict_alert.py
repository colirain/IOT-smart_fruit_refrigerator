#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Tingyu Li (tl2861)
# ---------------------------
from datetime import datetime
import time
import calendar
from collections import deque
import os
# boto3 s3
import boto3
import aws
from boto3.dynamodb.conditions import Key,Attr

# ml
import predict
from sqlalchemy import *

# initial s3
s3 = aws.getResource('s3', 'us-east-1')
dynamodb = aws.getResource('dynamodb', "us-east-1")
curtime = calendar.timegm(time.gmtime())

"""sns"""
client = aws.getClient("sns","us-east-1")
topic_arn = "arn:aws:sns:us-east-1:810588570945:fruit-alert"

# DIR = '/download_img/'

TIMEPOINTER = None

# IMG_QUE = deque(maxlen=100)

# expire csv
expire_table = dynamodb.Table('fruit-expire')


def download_img(filename):
    # bucket = s3.bucket('iotfruit')
    # # files = list(bucket.objects.filter())
    # obj = bucket.Objects(filename)
    # s3.download_file()
    # file_path =  filename
    # with open (file_path, 'w+') as f:
    s3.meta.client.download_file('iotfruit',filename, filename)
    # s3.meta.client.download_file('iotfruit', file_path, filename)

def delete_img(filename):
    os.remove(filename)
    s3.Object('iotfruit',filename).delete()



class dynamoMethods(object):
    """docstring for dynamoMethod"""
    def __init__(self, dbName):
        # super(dynamoMethod, self).__init__()
        self.table = dynamodb.Table(dbName)
        # self.predictList = []

    def get_image(self):
        """get image key from databse where haven't been predict"""
        predictList = []
        response = self.table.scan(FilterExpression=Attr('fruit_name').eq('NOT'))
        for i in response['Items']:
            print("the img to be download:{}".format(i['imgId']))
            download_img(i['imgId'])
            predictList.append(i['imgId'])
        return predictList

    def put_result(self, filenames, results):
        for i,filename in enumerate(filenames):
            #data = self.table.get_item(Key = {'imgId' : filename})
            #data['result'] = results[i]
            #data.save(overwrite=True)
            expire_period = expire_table.get_item(Key={'fruit_name':results[i]})['Item']['expire_period']
            print expire_period
            putin_date = self.table.get_item(Key={'imgId' : filename})['Item']['time_now']
            expire_date = int(putin_date) + int(expire_period)
            self.table.update_item(
                    Key={'imgId' : filename},
                    UpdateExpression="set fruit_name = :fruit_name, expire_date = :expire_date",
                    ExpressionAttributeValues={":fruit_name" : results[i], ":expire_date" : expire_date},
                    ReturnValues="UPDATED_NEW"
                    )
            delete_img(filename)


def real_time_predict():
    model = predict.TrainedModel()
    model.load_args()
    model.load_model()
    Table = dynamoMethods('fruit-img')
    try:
        while True:
            print ("new round")
            files = Table.get_image()
            print (files)
            if files != []:
                print 'start predict'
                results = model.predict(files)
                print results
                # results_dic = {}
                # for result in results:
                #     results_dic[]
                Table.put_result(files, results)
                print 'success put item in db'
            time.sleep(10)
    except Exception as e:
        print(e)

def get_out_of_date_fruit(alter_time):
    """get fruit older than curtime - alter_time*86400
    Args:
        alter_time (int):days before out of date
    Returns:
        dic :related dynamo database records
    """
    # fruit = []
    curtime = calendar.timegm(time.gmtime())
    table = dynamodb.Table('fruit-img')
    # print curtime
    threhold = curtime+alter_time
    response = table.scan(FilterExpression=Attr('expire_date').lt(threhold))
    # print response
    outFruit = {}
    for i in response['Items']:
        if i['machine'] not in outFruit.keys():
            outFruit[i['machine']] = [(i['fruit_name'],i['time_now'])]
        else:
            outFruit[i['machine']].append((i['fruit_name'],i['time_now']))
    print outFruit
    return outFruit

# def alter_user():
    """send alter to user"""


  


if __name__ == '__main__':
    get_out_of_date_fruit(30)
