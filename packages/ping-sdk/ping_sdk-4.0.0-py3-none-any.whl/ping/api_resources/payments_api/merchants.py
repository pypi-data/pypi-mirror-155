import requests
from ping.helper.apiHelper import json_deserialize, check_errors


def list(headers, base_url):
    #Does a GET request to /api/v1/merchants.

    #Lists merchants associated with a tenant. The merchant details
    #include email, id, name, organization number and phone number.

    #Args:
    #    None arguments.
    #Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = '/api/v1/merchants'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def create(headers, base_url, merchant_object):
    # Does a POST request to /api/v1/merchants.

    # Creates a new merchants for a tenant.
    # You must provide a object with the following values:
    # - "name"
    # - "organization_number"
    # Args(provided by the tenant):
    #   merchant_object (object, required): An object containing required merchant data.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = '/api/v1/merchants'
    _url = base_url + _path
    response = requests.post(_url, headers=headers, json=merchant_object)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def get(headers, base_url, merchant_id):
    # Does a GET request to /api/v1/merchants/{merchant_id}.

    # Provides details for a single merchant. The details include email, id,
    #name, organization name, organization number, phone number and status.

    # Args:
    #    merchant_id (string, required). The ID of the of the merchant to retrive.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = f'/api/v1/merchants/{merchant_id}'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # Deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result
