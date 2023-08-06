import requests
from ping.helper.apiHelper import json_deserialize, check_errors


def initiate(headers, base_url, payment_object, payment_order_id):
    #Does a POST request to '/api/v1/payment_orders/{payment_order_id}/payments.

    #Initiates a payment for a payment order.
    #Args (provided by the tenant):
    #  payment_object (object, required): An object containing all information needed to initiate a payment
    #  payment_order_id (string, required): An ID of a specific Payment Order
    #Returns:
    #  Response: A json object with the response value as well as other
    #  useful information such as status codes, headers and a potention error.


    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}/payments'
    _url = base_url + _path
    response = requests.post(_url, headers=headers, json=payment_object)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result


def get(headers, base_url, payment_order_id, payment_id):
    #Does a GET request to /api/v1/payment_orders/{payment_order_id}/payments/{payment_id}.

    #Retrieves a payment from a payment order
    #Args (provided by the tenant):
    #  payment_order_id (string, required): A string cointaining the ID of a specific payment order
    #  payment_id (string, required): A string cointaining the ID of a specific payment
    #Returns:
    #  Response: A json object with the response value as well as other
    #  useful information such as status codes, headers and a potention error.
    

    # Prepare and execute response
    _path = f'/api/v1/payment_orders/{payment_order_id}/payments/{payment_id}'
    _url = base_url + _path
    response = requests.get(_url, headers=headers)

    # deserialize and check errors
    decoded = json_deserialize(response.text)
    _result = check_errors(response, decoded)
    return _result
