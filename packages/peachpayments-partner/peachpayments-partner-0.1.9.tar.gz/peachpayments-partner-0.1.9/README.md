# Peach Partner Library

## Overview

**Peach Partner Library** is a platform-agnostic Python package to help Payment Service Providers in integrating with PeachPayments.

**Documentation**:

**Source Code**: <https://gitlab.com/peachpayments/peach-partner-python/>

* * *

### Key terms

| Term                     | Definition                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Partner API              | A service provided by Peach Payments to enable Payment Service Providers to become available on the Peach Platform |
| Payment Service Provider | A payment service provider who integrates with the Partner API                                                     |
| Outbound API call        | API calls sent from Partner API to the Payment Service Provider                                                    |
| Inbound API call         | API calls sent from Payment Service Provider to Partner API                                                        |

## Installation

Package requires Python 3.9+

```sh
# pip
$ pip3 install peachpayments-partner
```

```sh
# poetry
$ poetry add peachpayments-partner
```

## Result codes

```python
from peachpayments_partner.result_codes import result_codes

result_codes.TRANSACTION_SUCCEEDED.code == "000.000.000"
result_codes.get("000.000.000").name == "TRANSACTION_SUCCEEDED"
result_codes.get("000.000.000").description == "Transaction succeeded"
```

## Authentication

### Requests to Payment Service Provider

PeachPayments uses an authorization token (JWT) in each request made to the Payment Service Provider.
This library provides the `authentication.is_authenticated` method, which takes the token as an argument and the `authentication.get_key` to collect the signing_key.

The `is_authenticated` method has only one required argument, the token. If it's called without the optional `signing_key` it will collect the key using the `get_key` method. If it's called without the optional `audience` it will try to use the environment variable `AUTH0_AUDIENCE`.

The method decodes the token. If that succeeds, it returns `True`. Otherwise, it raises an `AuthError` exception.

## Formatting error responses

PeachPayments requires the error responses to be formatted in a specific way. This library provides the `format_error_response` method, which takes a dict containing error response as an argument and returns a formatted error response.

```python
def format_error_response(code, errors, data):
```
The `errors` dict might look like this:

```python
{
    "status": ["Not a valid string."],
    "code": ["Missing data for required field."],
}
```

The `data` dict might look like this:

```python
{
  "status": 10
}
```

With the `code` as `ResultCodes.INVALID_OR_MISSING_PARAMETER`, the formatted error response will look similar to this:

```python
{
    "result": {
      "code": "200.300.404",
      "description": "invalid or missing parameter",
      "parameterErrors": [
          {
              "value": 10,
              "name": "status",
              "message": "Not a valid string."
          },
          {
              "name": "code",
              "message": "Missing data for required field."
          }
      ]
  },
  "timestamp": "2021-08-03T16:16:30.992618Z"
}
```

## Fixtures

This library provides examples of valid requests and responses.

An example of the recommended usage for testing:

```python
import pytest
from copy import deepcopy
from peachpayments_partner.fixtures import DEBIT_RESPONSE

@pytest.fixture
def debit_response():
    return deepcopy(DEBIT_RESPONSE)
```