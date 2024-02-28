import requests
from pathlib import Path
import json


filepath = Path(__file__).parent / "config.json"

with open(filepath, 'r') as f:
    configJson = json.load(f)



def deleteMovie(tmdbId):

    response = getMovieInfo(tmdbId)
    radarrId = 0
    if response.status_code == 200:
        json_response = response.json()
        radarrId = json_response[0]['id']
    else:
        return "Error: "+str(response.status_code)


    RADARR_BASEURL = configJson["RADARR_BASEURL"]
    RADARR_APIKEY = configJson["RADARR_APIKEY"]
    url = RADARR_BASEURL+"movie/"+str(radarrId)+"?deleteFiles=true&addImportExclusion=false"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': RADARR_APIKEY,
    }
    return requests.delete(url, headers=headers)
    

def getMovieInfo(tmdbId):
    RADARR_BASEURL = configJson["RADARR_BASEURL"]
    RADARR_APIKEY = configJson["RADARR_APIKEY"]
    url = RADARR_BASEURL+"movie?tmdbId="+str(tmdbId)+"&excludeLocalCovers=false"
    headers = {
        'accept': 'application/json',
        'X-Api-Key': RADARR_APIKEY
    }
    return requests.get(url, headers=headers)

