---
title: "README"
excerpt: "A description the Ping Payments Python SDK"
---

# Ping Payments Python SDK

[![Tests](https://github.com/youcal/ping_python_sdk/actions/workflows/tests.yml/badge.svg)](https://github.com/youcal/ping_python_sdk/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/ping-sdk.svg)](https://badge.fury.io/py/ping-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The `Ping Payments Python SDK` manages the `Ping Payments API`.

## Table of contents

-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Ping Payments API](#payments-api)

## Requirements

The Ping Payments Python SDK supports the following versions of Python:

-   Python 3, versions 3.7 and later

## Installation

Install the latest Ping Payments Python SDK using pip:

```sh
pip install ping-sdk
```

## The [Ping Payments API]

The Ping Payments API is implemented as the `PaymentsApi` class. The PaymentsApi contains a number of endpoints.

### Ping Payments API Endpoints

Available endpoints in the PaymentApi class:

-   [Merchant]
-   [Payment Orders]
-   [Payment]
-   [Payout]
-   [Ping]

You work with the Ping Payments API by calling methods in the PaymentsApi endpoints.

The Ping Payments Python SDK documentation contains lists of available methods for each endpoint, on the page for each endpoint.

### Usage

Here’s how to get started with the Ping Payments API:

#### Get a tenant ID

Ping Payments provides you with a `tenant ID`. The Ping Payment API uses tenant IDs for resource permissions.

**Important:** Make sure you store and access the tenant ID securely.

Using the Ping Payments API:

-   Import the PaymentsAPI class.
-   Instantiate a PaymentsAPI object.
-   Initialize the PaymentsAPI object with the appropriate tenant ID and environment.

Detailed instructions:

1. Import the PaymentsApi class from the Ping Python SDK module:

```python

from ping.payments_api import PaymentsApi

```

2. Instantiate a PaymentsApi object and initialize it with the tenant ID and the environment that you want to use.

Initialize the PaymentsApi in production mode:

```python

payments_api = PaymentsApi(
		tenant_id = '55555555-5555-5555-5555-555555555555'
)

```

Initialize the PaymentsApi in sandbox mode, for testing:

```python

payments_api = PaymentsApi(
		tenant_id = '55555555-5555-5555-5555-555555555555',
		environment = 'sandbox'
)

```

You can ping the API to see if it's accessible. A working response contains the text "pong".

```python

payments_api.ping.ping_the_api()

```

#### Get an Instance of an PaymentsApi Object and Call the Methods of the PaymentsApi class

**Work with the API by calling the methods on the API object.** For example, you call `list()` for a list of all merchants connected to a tenant:

```python

result = payments_api.merchant.list()

```

#### Handle the response

Calls to the Ping Payments API endpoint methods return an ApiResponse object. Properties of the ApiResponse object describe the request (headers and request) and the response (status_code, reason_phrase, text, errors, body, and cursor).

Using the response:

**Check whether the response succeeded or failed.** Two helper methods in the ApiResponse object determine the success or failure of a call:

```python

if result.is_success():
	# Display the response as text
	print(result.text)
# Call the error method to see if the call failed
elif result.is_error():
	print(f"Errors: {result.errors}")

```

[//]: # "Link anchor definitions"
[ping payments api]: doc/payments_api.md
[merchant]: doc/api_resources/payments_api/merchant.md
[payment orders]: doc/api_resources/payments_api/paymentOrder.md
[payment]: doc/api_resources/payments_api/payment.md
[payout]: doc/api_resources/payments_api/payout.md
[ping]: doc/api_resources/payments_api/ping.md
