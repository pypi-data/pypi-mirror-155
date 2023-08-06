import requests
from ping.helper.apiHelper import json_deserialize, check_errors


def list(headers, base_url, date_from, date_to):
    #Does a GET request to /api/v1/payment_orders.

    #Retrieves a list of payment orders.
    #Args (provided by the tenant):
    #  date_from (string, optional): The timestamp for the beginning of
    #    the reporting period, in RFC 3339 format. Default: None
    #  date_to (string, optional): The timestamp for the end of
    #    the reporting period, RFC 3339 format. Default: None
    #Returns:
    #  Response: A json object with the response value as well as other
    #  useful information such as status codes, headers and a potention error.
    

    _path = '/api/v1/payment_orders'

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


def create(headers, base_url, split_tree_id, currency):
    # Does a POST request to /api/v1/payment_orders.

    # Creates a new payment order.
    # Args (provided by the tenant):
    #    split_tree_id (string, required): An string with a valid split tree ID.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = '/api/v1/payment_orders'
    _url = base_url + _path
    _payload = {
        "split_tree_id": split_tree_id,
        "currency": currency
    }
    response = requests.post(_url, headers=headers, json=_payload)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def get(headers, base_url, payment_order_id):
    # Does a GET request to /api/v1/payment_orders/{payment_order_id}.

    # Retrives a specific payment order.
    # Args (provided by the tenant):
    #    payment_order_id (String, required): The ID of the of the payment order to retrive.
    # Returns:
    #    Response: A json object with the response value as well as other
    

    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def update(headers, base_url, payment_order_id, split_tree_id):
    # Does a PUT request to /api/v1/payment_orders/{payment_order_id}.

    # Updates the split tree of a specific payment order.
    # Args (provided by the tenant):
    #    payment_order_id (String, required): The ID of the of the payment order to update.
    #    split_tree_id (String, required): An string with a valid split tree ID.
    # Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}'
    _url = base_url + _path
    _payload = {
        "split_tree_id": split_tree_id
    }
    response = requests.put(_url, headers=headers, json=_payload)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def close(headers, base_url, payment_order_id):
    # Does a PUT request to /api/v1/payment_orders/{payment_order_id}/close'.

    # Closes a specific payment order.
    # Args (provided by the tenant):
    #    payment_order_id (String, required): The ID of the of the payment order to close.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}/close'
    _url = base_url + _path
    response = requests.put(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result

def split(headers, base_url, payment_order_id, fast_forward):
    # Does a PUT request to /api/v1/payment_orders/{payment_order_id}/split.

    # Split a specific payment order.
    # Args (provided by the tenant):
    #    payment_order_id (String, required): The ID of the of the payment order to split.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}/split'
    _url = base_url + _path

    if fast_forward == True:
        _payload = {
            "fast_forward": fast_forward
        }
        response = requests.put(_url, headers=headers, json=_payload)
    else:
        response = requests.put(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def settle(headers, base_url, payment_order_id, fast_forward):
    # Does a PUT request to /api/v1/payment_orders/{payment_order_id}/settle'.

    # Settle a specific payment order.
    # Args (provided by the tenant):
    #    payment_order_id (String, required): The ID of the of the payment order to settle.
    # Returns:
    #    Response: A json object with the response value as well as other
    #    useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}/settle'
    _url = base_url + _path
    
    if fast_forward == True:
        _payload = {
            "fast_forward": fast_forward
        }
        response = requests.put(_url, headers=headers, json=_payload)
    else:
        response = requests.put(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result
