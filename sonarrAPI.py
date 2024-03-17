
import requests
from pathlib import Path
import json


filepath = Path(__file__).parent / "config.json"

with open(filepath, 'r') as f:
    configJson = json.load(f)


def deleteShow(tmdbId):
    SONARR_BASEURL = configJson["SONARR_BASEURL"]
    SONARR_APIKEY = configJson["SONARR_APIKEY"]
    url = SONARR_BASEURL+"series/"+str(tmdbId)+"?deleteFiles=true&addImportListExclusion=false"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': SONARR_APIKEY
    }
    return requests.delete(url, headers=headers)

def getShowInfo(tmdbId):
    SONARR_BASEURL = configJson["SONARR_BASEURL"]
    SONARR_APIKEY = configJson["SONARR_APIKEY"]
    url = SONARR_BASEURL+"series?tvdbId="+str(tmdbId)+"&includeSeasonImages=false"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': SONARR_APIKEY
    }
    return requests.get(url, headers=headers)

def getEpisodeFiles(serieID):
    SONARR_BASEURL = configJson["SONARR_BASEURL"]
    SONARR_APIKEY = configJson["SONARR_APIKEY"]
    url = SONARR_BASEURL+"episodefile?seriesId="+str(serieID)+"&episodeFileIds=1"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': SONARR_APIKEY
    }
    return requests.get(url, headers=headers)

def deleteEpisodeFile(episodeFileId):
    SONARR_BASEURL = configJson["SONARR_BASEURL"]
    SONARR_APIKEY = configJson["SONARR_APIKEY"]
    url = SONARR_BASEURL+"episodefile/"+str(episodeFileId)
    headers = {
        'accept': 'application/json',
        'X-Api-Key': SONARR_APIKEY
    }
    return requests.delete(url, headers=headers)

def updateShow(serieID, data):
    SONARR_BASEURL = configJson["SONARR_BASEURL"]
    SONARR_APIKEY = configJson["SONARR_APIKEY"]
    url = SONARR_BASEURL+"series/"+str(serieID)+"?moveFiles=false"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': SONARR_APIKEY
    }
    return requests.put(url, headers=headers, json=data)


def episodeMonitor(episodeIDs, monitored):
    episodestoUpdate = []
    episodestoUpdate =episodeIDs
    SONARR_BASEURL = configJson["SONARR_BASEURL"]
    SONARR_APIKEY = configJson["SONARR_APIKEY"]
    url = SONARR_BASEURL+"/api/v3/episode/monitor?includeImages=false"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': SONARR_APIKEY
    }
    data = {
        "episodeIds": episodestoUpdate,
        "monitored": monitored
    }
    return requests.put(url, headers=headers, json=data)
