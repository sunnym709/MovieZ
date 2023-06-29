import requests
import json

def searchDb(collection,sort={},filter={},skip=None,limit=None):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-jktzb/endpoint/data/v1/action/find"
    payload = json.dumps({
        "collection": collection,
        "database": "api",
        "dataSource": "Cluster0",
        "filter": filter,
        "sort": sort,
        "limit": limit,
        "skip": skip,})
    headers = {
      'Content-Type': 'application/json',
      'Access-Control-Request-Headers': '*',
      'api-key': 'oEMu1rIsWSQgMm20dBo9av7uQ1FxIvtNgvR61QwjmcmqEuxAOyIGGl0VwS4QftiA',
    }
    return requests.request("POST", url, headers=headers, data=payload).json().get('documents')


def updateDb(channel,Id,title):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-jktzb/endpoint/data/v1/action/updateOne"
    payload = json.dumps({
        "collection": channel,
        "database": "api",
        "dataSource": "Cluster0",
        "filter": {"Id": Id},
        "update": {"$set": {"title": title}}
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'oEMu1rIsWSQgMm20dBo9av7uQ1FxIvtNgvR61QwjmcmqEuxAOyIGGl0VwS4QftiA',
    }
    requests.request("POST", url, headers=headers, data=payload)


def deleteDb(channel,Id):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-jktzb/endpoint/data/v1/action/deleteOne"
    payload = json.dumps({
        "collection": channel,
        "database": "api",
        "dataSource": "Cluster0",
        "filter": {"Id": Id},
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'oEMu1rIsWSQgMm20dBo9av7uQ1FxIvtNgvR61QwjmcmqEuxAOyIGGl0VwS4QftiA',
    }
    requests.request("POST", url, headers=headers, data=payload)


def addDb(document):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-jktzb/endpoint/data/v1/action/insertOne"
    payload = json.dumps({
        "collection": "TMDB",
        "database": "api",
        "dataSource": "Cluster0",
        "document":document
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'oEMu1rIsWSQgMm20dBo9av7uQ1FxIvtNgvR61QwjmcmqEuxAOyIGGl0VwS4QftiA',
    }
    requests.request("POST", url, headers=headers, data=payload)

def indexDb(filter={},skip=None,limit=None):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-jktzb/endpoint/data/v1/action/find"
    payload = json.dumps({
        "collection": "tmdb",
        "database": "api",
        "dataSource": "Cluster0",
        "filter": filter,
        "sort": {"Id": -1},
        "limit": limit,
        "skip": skip, })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'oEMu1rIsWSQgMm20dBo9av7uQ1FxIvtNgvR61QwjmcmqEuxAOyIGGl0VwS4QftiA',
    }
    return requests.request("POST", url, headers=headers, data=payload).json().get('documents')


def postDb(Id):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-jktzb/endpoint/data/v1/action/findOne"
    payload = {
        "collection": "tmdb",
        "database": "api",
        "dataSource": "Cluster0",
        "filter": {"Id":Id},
        "projection": {"_id": 0, "Id": 0}
    }
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'oEMu1rIsWSQgMm20dBo9av7uQ1FxIvtNgvR61QwjmcmqEuxAOyIGGl0VwS4QftiA',
    }
    return requests.request("POST", url, headers=headers, json=payload).json().get('document')
