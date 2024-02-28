import json
import re
import overseerrAPI
import radarrAPI
import sonarrAPI
import loggerManager
import webhookCaller
from pathlib import Path

filepath = Path(__file__).parent / "config.json"

with open(filepath, 'r') as f:
    configJson = json.load(f)


logger = loggerManager.get_module_logger("helpers.py")
#General
def deleteMovie(movieInfo):
    response = radarrAPI.deleteMovie(movieInfo.tmdbId)
    if response.status_code == 200:
        responseOverseerr = overseerrAPI.deleteRequest(movieInfo.overseerRequestId)
        if responseOverseerr.status_code == 200 and responseOverseerr.status_code != 204:
            return "Movie Deleted from Radarr and Overseer"
    else:
        logger.error(f"Error: {response.status_code}")
        logger.error(response.text)

def processShowDeletion(showOBJ):
    showInfoResponse = sonarrAPI.getShowInfo(showOBJ.tvdbId)
    if showInfoResponse.status_code != 200:        
        logger.error(f"Error: {showInfoResponse.status_code}")
        logger.error(showInfoResponse.text)
    json_showInfoResponse = showInfoResponse.json()
    if len(json_showInfoResponse) == 0:
        return "Show not found in Sonarr"
    else:
        logger.info("Processing " +json_showInfoResponse[0]['title'])
        showOBJ.overseerRequestAlreadyDeleted = False
        showOBJ.radarrSeriesId = json_showInfoResponse[0]['id']
        showStatus = json_showInfoResponse[0]['status']
        numberofseasonsmonitored = 0
        seasonNumber = 0
        for season in json_showInfoResponse[0]['seasons']:
            logger.info(f"Seasons Number: {season['seasonNumber']}")
            logger.info(f"Season Monitored?: {season['monitored']}")
            logger.info("===================================")

            statisticsExist = 'statistics' in season
            statistics = season['statistics']
            nextAiringExist = 'nextAiring' in statistics
            if statisticsExist:
                nextAiringExist = 'nextAiring' in statistics
                if nextAiringExist:
                    nextAiring = statistics['nextAiring']
                    logger.info(f"Next nextAiring:{nextAiring}")
                    return "Show have a next airing in the season skip deletion"
            else:
                logger.info("No statistics found in the season")
            seasonNumber += 1
            
        if numberofseasonsmonitored == 0 and showStatus == "ended":
            logger.info("No Seasons monitored and ended")
            responseDeleteRequest = sonarrAPI.deleteShow(showOBJ.radarrSeriesId)
            if responseDeleteRequest.status_code != 200:        
                logger.error(f"Error: {responseDeleteRequest.status_code}")
                logger.error(responseDeleteRequest.text)
            else:
                logger.info("Show deleted from Sonarr")

                if showOBJ.overseerRequestAlreadyDeleted == False:
                    responseOverserrDeleteRequest = overseerrAPI.deleteRequest(showOBJ.overseerRequestId)
                    showOBJ.overseerRequestAlreadyDeleted = True
                    if responseOverserrDeleteRequest.status_code != 200 and responseOverserrDeleteRequest.status_code != 204:        
                        logger.error(f"Error: {responseOverserrDeleteRequest.status_code}")
                        logger.error(responseOverserrDeleteRequest.text)
                    return "Show Deleted from Sonarr and Overseer"
                    
        if numberofseasonsmonitored == 0 and showStatus == "continuing":
            logger.info("No Seasons monitored and continuing")
            logger.info("Deleting request from overseer to allow the user to request again")
            if showOBJ.overseerRequestAlreadyDeleted == False:
                responseDeleteRequest = overseerrAPI.deleteRequest(showOBJ.overseerRequestId)
                showOBJ.overseerRequestAlreadyDeleted = True
                if responseDeleteRequest.status_code != 200 and responseDeleteRequest.status_code != 204:        
                    logger.error(f"Error: {responseDeleteRequest.status_code}")
                    logger.error(responseDeleteRequest.text)
                else:
                    return "Request Deleted from Overseer and show continuing "
        
        logger.info("--------------------")


def getJsonsPropertie(json, propertie):
    if propertie in json:
        return json[propertie]
    else:
        return None


def wasWatchedOnlyByRequester(obj):
    mediaWatchData = overseerrAPI.getMediaWatchData(obj.mediaId)
    if mediaWatchData.status_code != 200:
        logger.error(f"Error: {mediaWatchData.status_code}")
        logger.error(mediaWatchData.text)
    else:
        json_mediaWatchData = mediaWatchData.json()
        if 'data' in json_mediaWatchData:
            if len(json_mediaWatchData['data']['users']) == 0:
                return False
            else:
                for userWatchData in json_mediaWatchData['data']['users']:
                    logger.info(f"Watched by {userWatchData['username']} and requested by {obj.requestedby}")
                    
                    if(userWatchData['username'] != obj.requestedby):
                        return False
                return True
        else:
            logger.info("Media Not avaialable yet")
            return False
    
def notifyWithDeletionItens(itensToDeleteList):
    message = "The following itens were deleted from Overseer and Radarr/Sonarr:\\n\\n"
    for item in itensToDeleteList:
        message += f"Type: {item.mediaType}\\n"
        message += f"ServiceUrl: {item.serviceUrl}\\n"
        message += f"Requested by: {item.requestedby}\\n"
        message += f"CreatedAt: {item.createdAt}\\n"
        message += f"Last Change: {item.dateToCheck}\\n"
        message += f"DaysPassed: {item.daysPassed}\\n"
        message += f"SeasonsInRequest: {item.seasonsInRequest}\\n"
        message += f"===================================\\n"
        
    jsonMessage = {
            "message": message
        }
    

    WEBHOOK = configJson["WEBHOOK"]
    
    webhookCaller.sendWebhook(WEBHOOK,jsonMessage)

def notifyDeletionWarning(itensToDeleteList):
    message = "The following itens will be deleted from Overseer and Radarr/Sonarr in the next run:\\n\\n"
    shouldSendMessage = False

    for item in itensToDeleteList:
        if item.daysToDelete - item.daysPassed >= 1:
            continue
        
        shouldSendMessage = True
        message += f"Type: {item.mediaType}\\n"
        message += f"ServiceUrl: {item.serviceUrl}\\n"
        message += f"Requested by: {item.requestedby}\\n"
        message += f"CreatedAt: {item.createdAt}\\n"
        message += f"Last Change: {item.dateToCheck}\\n"
        message += f"DaysPassed: {item.daysPassed}\\n"
        message += f"SeasonsInRequest: {item.seasonsInRequest}\\n"
        message += f"===================================\\n"
        
    jsonMessage = {
            "message": message
    }
    

    WEBHOOK = configJson["WEBHOOK"]
    if shouldSendMessage:
        webhookCaller.sendWebhook(WEBHOOK,jsonMessage)

def sendNotification(message):
    jsonMessage = {
            "message": message
    }
    WEBHOOK = configJson["WEBHOOK"]
    webhookCaller.sendWebhook(WEBHOOK,jsonMessage)

def parse_crontab_file(file_path):
    cron_config = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('// BEGIN:'):
                cron_config.append(line.strip().split(':')[-1])
            elif line.startswith('// END:'):
                cron_config.append(line.strip().split(':')[-1])
            elif line.startswith('0'):
                cron_config.append(line.strip())

    # Use regular expression to extract the cron value
    cron_pattern = r'(\S+ \S+ \S+ \S+ \S+)'
    matches = re.findall(cron_pattern, cron_config[0])

    if matches:
        cron_value = matches[0]
        print(cron_value)
    else:
        return "No cron value found."
    return cron_value


def is_valid_url(url):
    url_pattern = r'^(http|https)://[^\s/$.?#].[^\s]*$'
    return re.match(url_pattern, url) is not None