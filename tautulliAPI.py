import requests
import datetime
import loggerManager
from pathlib import Path
import json


filepath = Path(__file__).parent / "config.json"

with open(filepath, 'r') as f:
    configJson = json.load(f)


logger = loggerManager.get_module_logger("tautulliAPI.py")

def getHistory(rating_key_type,rating_key, length):
    TAUTULLI_BASEURL = configJson["TAUTULLI_BASEURL"]
    TAUTULLI_APIKEY = configJson["TAUTULLI_APIKEY"]

    url = TAUTULLI_BASEURL+"?apikey="+TAUTULLI_APIKEY+"&cmd=get_history&"+rating_key_type+"="+str(rating_key)+"&length="+str(length)
    headers = {
        'accept': 'application/json',
    }
    return requests.get(url, headers=headers)

def get_children_metadata(rating_key):
    TAUTULLI_BASEURL = configJson["TAUTULLI_BASEURL"]
    TAUTULLI_APIKEY = configJson["TAUTULLI_APIKEY"]

    url = TAUTULLI_BASEURL+"?apikey="+TAUTULLI_APIKEY+"&cmd=get_children_metadata&rating_key="+str(rating_key)
    headers = {
        'accept': 'application/json',
    }
    return requests.get(url, headers=headers)

def getTV_History(rating_key,season):
    childrenMetadata = get_children_metadata(rating_key)
    if childrenMetadata.status_code == 200:
        json_childrenMetadata = childrenMetadata.json()
        for children_list in json_childrenMetadata['response']['data']['children_list']:
            
            if children_list['media_index'] == str(season):
                return getHistory('parent_rating_key',children_list['rating_key'],1)
                

    else:
        logger.error(f"Error: {childrenMetadata.status_code}")
        logger.error(childrenMetadata.text)

def wasWatchedInPastDays(obj,NUMBER_OF_DAYS):
    returnObject = type('', (), {})()
    today = datetime.datetime.now()
    date_time_obj = datetime.datetime.strptime(obj.dateToCheck, '%Y-%m-%dT%H:%M:%S.%fZ')
    if obj.mediaType == 'tv':
        seasonHistory = getTV_History(obj.rating_key,obj.season)
        if seasonHistory == None:
            dayspassed = (today - date_time_obj).days
            returnObject.daysPassed = dayspassed
            if dayspassed >= NUMBER_OF_DAYS:
                returnObject.wasWatched = False
                return returnObject
            returnObject.wasWatched = True
            return returnObject
        if seasonHistory.status_code != 200:
            logger.error(f"Error: {seasonHistory.status_code}")
            logger.error(seasonHistory.text)
            returnObject.wasWatched = False
            return returnObject
        
        json_seasonHistory = seasonHistory.json()

        if json_seasonHistory['response']['data']['data'] == []:
            dayspassed = (today - date_time_obj).days
            logger.info(f"Days Passed: {dayspassed} of {NUMBER_OF_DAYS} days")
            returnObject.daysPassed = dayspassed
            if dayspassed >= NUMBER_OF_DAYS:
                returnObject.wasWatched = False
                return returnObject
            returnObject.wasWatched = True
            return returnObject 
        result = json_seasonHistory['response']['data']['data'][0]
        dateEpoch = int(result['date'])
        activityDate = datetime.datetime.fromtimestamp(dateEpoch)
        dayspassed = (today - activityDate).days
        logger.info(f"Days Passed: {dayspassed} of {NUMBER_OF_DAYS} days")
        returnObject.daysPassed = dayspassed
        if dayspassed >= NUMBER_OF_DAYS:
            returnObject.wasWatched = False
            return returnObject
        else:
            returnObject.wasWatched = True
            return returnObject
    if obj.mediaType == 'movie':
        history = getHistory('rating_key',obj.rating_key,1)
        if history.status_code != 200:
            logger.error(f"Error: {history.status_code}")
            logger.error(history.text)
            returnObject.wasWatched = False
            return returnObject
        json_history = history.json()
        if json_history['response']['data']['data'] == []:
            date_time_obj = datetime.datetime.strptime(obj.dateToCheck, '%Y-%m-%dT%H:%M:%S.%fZ')
            dayspassed = (today - date_time_obj).days
            logger.info(f"Days Passed: {dayspassed} of {NUMBER_OF_DAYS} days")
            returnObject.daysPassed = dayspassed
            if dayspassed >= NUMBER_OF_DAYS:
                returnObject.wasWatched = False
                return returnObject
            returnObject.wasWatched = True
            return returnObject
        result = json_history['response']['data']['data'][0]
        dateEpoch = int(result['date'])
        activityDate = datetime.datetime.fromtimestamp(dateEpoch)
        dayspassed = (today - activityDate).days
        returnObject.daysPassed = dayspassed
        logger.info(f"Days Passed: {dayspassed} of {NUMBER_OF_DAYS} days")
        if (today - activityDate).days >= NUMBER_OF_DAYS:
            returnObject.wasWatched = False
            return returnObject
        else:
            returnObject.wasWatched = True
            return returnObject
        
