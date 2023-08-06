import requests
from ping.helper.apiHelper import json_deserialize, check_errors


def ping_the_api(headers, base_url):
    #Does a GET request to /api/v1/ping.

    #Ping the API to verify that it is reachable

    #Args:
    #    None arguments.
    #Returns:
    #    Response: returns "Pong" if the API is reachable
    

    # Prepare and execute response
    _path = '/api/v1/ping'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result