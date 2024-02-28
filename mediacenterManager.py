# Import the functions from the example_functions module
import copy
import helpers
import tautulliAPI
import overseerrAPI
import constants
import loggerManager
from pathlib import Path
import json
# Importing the constants module

#overseer get requests
# tautily get play history by season
# delete de todo o lado

##teste tautulli

try:
    filepath = Path(__file__).parent / "config.json"

    with open(filepath, 'r') as f:
        configJson = json.load(f)



    crontab_path = Path(__file__).parent / "crontab"
    cron_config = helpers.parse_crontab_file(crontab_path)


    USERS_TO_IGNORE = configJson["USERS_TO_IGNORE"]



    logger = loggerManager.get_module_logger("MediacenterPurger.py")

    logger.info(f"Media center Purger starting")

    useWebhook = helpers.is_valid_url(configJson["WEBHOOK"])
    if useWebhook == False:
        logger.info(f"Invalid Webhook URL, bypassing notifications")
        exit()
    if helpers.is_valid_url(configJson["OVERSEER_BASEURL"]) == False:
        logger.error(f"Invalid Overseerr API URL")
        exit()
    if helpers.is_valid_url(configJson["RADARR_BASEURL"]) == False:
        logger.error(f"Invalid Tautulli API URL")
        exit()
    if helpers.is_valid_url(configJson["TAUTULLI_BASEURL"]) == False:
        logger.error(f"Invalid Radarr API URL")
        exit()
    if helpers.is_valid_url(configJson["SONARR_BASEURL"]) == False:
        logger.error(f"Invalid Sonarr API URL")
        exit()
    



    getallMediaAvailable ='media?take=1000&skip=0&filter=available&sort=added'
    getallMediaPartial ='media?take=1000&skip=0&filter=partial&sort=added'


    getProcessingRequests = 'request?take=2000&filter=processing&sort=added'
    getAvailableRequests = 'request?take=2000&filter=available&sort=added'

    allProcessingrequests = overseerrAPI.getData(getProcessingRequests)
    allAvailablegrequests = overseerrAPI.getData(getAvailableRequests)

    if allProcessingrequests.status_code != 200:
        # There was an error in the request
        raise Exception(f"Error: {allProcessingrequests.status_code}\n{allProcessingrequests.text}\nError: {allAvailablegrequests.status_code}\n{allAvailablegrequests.text}\nFull Response:{allAvailablegrequests}")
    if allAvailablegrequests.status_code != 200:
        raise Exception(f"\nError: {allAvailablegrequests.status_code}\n{allAvailablegrequests.text}\nError: {allAvailablegrequests.status_code}\n{allAvailablegrequests.text}\nFull Response:{allAvailablegrequests}")
    

    overseerrRequestList = []
    overseerrRequestList.extend(allProcessingrequests.json()['results'])
    overseerrRequestList.extend(allAvailablegrequests.json()['results'])



    itensToCheck = []
    obj = type('', (), {})()
    # The request was successful, and you can access the response content
    for overseerrRequest in overseerrRequestList:
        #logger.info(f"===================================")
        media=overseerrRequest['media']
        #if helpers.getJsonsPropertie(media,'ratingKey') == None:
        #    logger.info(f"skipping ", media['mediaType'], media['externalServiceSlug'], media['status'])
        #    continue

        
        logger.info(f"Type: {media['mediaType']}")
        logger.info(f"externalServiceSlug: {media['externalServiceSlug']}")
        logger.info(f"Status: {constants.mediaAvailability[media['status']]}")
        logger.info(f"serviceUrl: {media['serviceUrl']}")
        
        if (media['status'] == 2 or media['status'] == 3 ) and media['mediaType'] == 'movie':
            logger.info(f"Movie: {media['serviceUrl']} not yet available status {constants.mediaAvailability[media['status']]} , skipping")
            continue
        
        obj = type('', (), {})()
        obj.overseerRequestId = overseerrRequest['id']
        obj.tmdbId = media['tmdbId']
        obj.tvdbId = media['tvdbId']
        obj.mediaType = media['mediaType']
        obj.createdAt = media['createdAt']
        obj.mediaAddedAt = media['mediaAddedAt']
        if helpers.getJsonsPropertie(media,'mediaAddedAt') != None:
            obj.dateToCheck = media['mediaAddedAt']
        else:
            obj.dateToCheck = media['createdAt']
        obj.mediaId = media['id']
        obj.serviceUrl = media['serviceUrl']
        obj.rating_key = media['ratingKey']
        obj.seasonsInRequest = len(overseerrRequest['seasons'])
        obj.externalServiceSlug = media['externalServiceSlug']
        obj.requestedby = overseerrRequest['requestedBy']['username']
        if media['mediaType'] == 'tv':
            for season in overseerrRequest['seasons']:
                #logger.info(f"########")
                #logger.info(f"Seasons ID: {season['id']}")
                #logger.info(f"Seasons Number: {season['seasonNumber']}")
                #logger.info(f"Season request status:  {constants.requestsStatus[season['status']]}")
                #logger.info(f"Season status:  {overseerrRequest['requestedBy']['username']}")
                obj.season = season['seasonNumber']
                #logger.info(f"########")
        
        itensToCheck.append(obj)
        #logger.info(f"===================================")



    
    itensToDelete = []
    itensNotDelete = []
    logger.info(f"Checking If the media was watched in the past days")
    for obj in itensToCheck:
        NUMBER_OF_DAYS = int(configJson["NUMBER_OF_DAYS"])
        logger.info(f"===================================")
        logger.info(f"Checkif For: "+ obj.externalServiceSlug)
        logger.info(f"requestedby: "+ obj.requestedby)
        logger.info(f"mediaType: "+ obj.mediaType)
        logger.info(f"dateToCheck: "+ obj.dateToCheck)
        logger.info(f"requestedby: "+ obj.requestedby)

        whatchedOnlyByRequester = helpers.wasWatchedOnlyByRequester(obj)
        logger.info(f"whatchedOnlyByRequester: {whatchedOnlyByRequester}")
        if whatchedOnlyByRequester:
            logger.info(f"Watched only by requester")
            NUMBER_OF_DAYS = int(configJson["NUMBER_OF_DAYS_IF_ONLY_REQUESTER"])
        if obj.requestedby in USERS_TO_IGNORE:
            logger.info(f"Ignoring User: "+ obj.requestedby)
            continue
        wasWatchedInPastDays = tautulliAPI.wasWatchedInPastDays(obj,NUMBER_OF_DAYS)
        cloned_obj = copy.deepcopy(obj)
        cloned_obj.daysPassed = wasWatchedInPastDays.daysPassed
        cloned_obj.daysToDelete = NUMBER_OF_DAYS
        if wasWatchedInPastDays.wasWatched:
            itensNotDelete.append(cloned_obj)
            logger.info(f"Not To Delete")
        else:
            logger.info(f"To Delete")
            itensToDelete.append(cloned_obj) 

        logger.info(f"===================================")

    if len(itensNotDelete) != 0 and useWebhook:
        helpers.notifyDeletionWarning(itensToDelete)

    logger.info(f"Deletions Required: {len(itensToDelete)}")
    deletionsExecuted = 0
    if len(itensToDelete) == 0 and useWebhook:
        logger.info(f"No Deletions required")
        helpers.sendNotification(f"No Deletions required, see you tomorrow at {cron_config}!")
        exit()
    if useWebhook:
        helpers.notifyWithDeletionItens(itensToDelete)
    
    TESTING_MODE = int(configJson["TESTING_MODE"])
    if TESTING_MODE == 1:
        logger.info(f"TESTING MODE: EXITING")
        exit() #remove to Delete
    for obj in itensToDelete:
        
        logger.info(f"-----------------------------------")
        logger.info(f"Checkif For: "+ obj.externalServiceSlug)
        logger.info(f"requestedby: "+ obj.requestedby)
        logger.info(f"mediaType: "+ obj.mediaType)
        logger.info(f"dateToCheck: "+ obj.dateToCheck)
        logger.info(f"requestedby: "+ obj.requestedby)

        if(obj.mediaType == 'movie'):        
            response = helpers.deleteMovie(obj)
            logger.info(response)
        if(obj.mediaType == 'tv'):
            response = helpers.processShowDeletion(obj)
            logger.info(response)
        deletionsExecuted += 1
        logger.info(f"-----------------------------------")

    logger.info(f"Deletions Executed: {deletionsExecuted}")
    logger.info(f"Media center Purger finished")
        
except Exception as e:
  # code to handle the exception
  logger.error(f"An error occurred: {e}")
  if useWebhook:
    helpers.sendNotification(e)