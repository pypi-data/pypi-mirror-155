import requests

api_key = None
RUBBRBAND_URL = "https://api.rubbrband.com"

def store(key, value):
    if api_key:
        response = requests.post(RUBBRBAND_URL + "/put/" + key + "?api_key=" + api_key, json=value)
        return response
    else:
        return {
            "error" : "No API Key provided! Call init on your rubbrband instance with a valid key."
        }

def replay(key):
    if api_key:
        response = requests.get(RUBBRBAND_URL + "/get/" + key + "?api_key=" + api_key)
        return response
    else:
        return {
            "error" : "No API Key provided! Call init on your rubbrband instance with a valid key."
        }

def delete(key):
    if api_key:
        response = requests.post(RUBBRBAND_URL + "/delete/" + key + "?api_key=" + api_key)
        return response
    else:
        return {
            "error" : "No API Key provided! Call init on your rubbrband instance with a valid key."
        }
