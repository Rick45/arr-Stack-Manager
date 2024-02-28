import requests
from pathlib import Path
import json


#Availability of the media. 1 = UNKNOWN, 2 = PENDING, 3 = PROCESSING, 4 = PARTIALLY_AVAILABLE, 5 = AVAILABLE
#Status of the request. 1 = PENDING APPROVAL, 2 = APPROVED, 3 = DECLINED

filepath = Path(__file__).parent / "config.json"

with open(filepath, 'r') as f:
    configJson = json.load(f)


def getData(action):
    OVERSEER_BASEURL = configJson["OVERSEER_BASEURL"]
    OVERSEER_TOKEN = configJson["OVERSEER_TOKEN"]
    url = OVERSEER_BASEURL+action
    headers = {
        'accept': 'application/json',
        'X-Api-Key': OVERSEER_TOKEN,
    }
    return requests.get(url, headers=headers)

def deleteRequest(requestId):
    OVERSEER_BASEURL = configJson["OVERSEER_BASEURL"]
    OVERSEER_TOKEN = configJson["OVERSEER_TOKEN"]
    url = OVERSEER_BASEURL+"request/"+str(requestId)
    headers = {
        'accept': 'application/json',
        'X-Api-Key': OVERSEER_TOKEN
    }
    
    return requests.delete(url, headers=headers)

def deleteMedia(mediaId):
    OVERSEER_BASEURL = configJson["OVERSEER_BASEURL"]
    OVERSEER_TOKEN = configJson["OVERSEER_TOKEN"]
    url = OVERSEER_BASEURL+"media/"+str(mediaId)
    headers = {
        'accept': 'application/json',
        'X-Api-Key': OVERSEER_TOKEN
    }
    return requests.delete(url, headers=headers)

def getMediaWatchData(mediaId):
    OVERSEER_BASEURL = configJson["OVERSEER_BASEURL"]
    OVERSEER_TOKEN = configJson["OVERSEER_TOKEN"]
    url = OVERSEER_BASEURL+"media/"+str(mediaId)+"/watch_data"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': OVERSEER_TOKEN
    }
    return requests.get(url, headers=headers)