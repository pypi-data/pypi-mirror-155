import requests
from ping.helper.apiHelper import json_deserialize, check_errors


def list(headers, base_url, date_from, date_to):
    #Does a GET request to /api/v1/payment_orders.

    #Retrieves a list of payouts.
    #Args (provided by the tenant):
    #  date_from (string, optional): The timestamp for the beginning of
    #    the reporting period, in RFC 3339 format. Default: None
    #  date_to (string, optional): The timestamp for the end of
    #    the reporting period, RFC 3339 format. Default: None
    #Returns:
    #  Response: A json object with the response value as well as other
    #  useful information such as status codes, headers and a potention error.
    

    _path = '/api/v1/payouts'

    # checks for possible query parameters
    if date_from and date_to is None:
        _path = _path + f'?from={date_from}'
    elif date_to and date_from is None:
        _path = _path + f'?to={date_to}'
    elif date_from and date_to:
        _path = _path + f'?from={date_from}&to={date_to}'

    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result

def get(headers, base_url, payout_id):
    # Does a GET request to /api/v1/payouts/{payout_id}.

    # Retrives a specific payout.
    # Args (provided by the tenant):
    #    payout_id (String, required): The ID of the of the payout to retrive.
    # Returns:
    #    Response: A json object with the response value as well as other
    #  useful information such as status codes, headers and a potention error.

    # Prepare and execute response
    _path = f'/api/v1/payouts/{payout_id}'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result