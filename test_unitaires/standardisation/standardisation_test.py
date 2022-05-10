import pytest
import requests
import base64

# définition de l'adresse de l'API
api_address = 'bank_api_classifier'
# port de l'API
api_port = 8000
# url to get the user
url='http://{address}:{port}/standardisation'.format(address=api_address, port=api_port)

# header with credentials
username = "admin"
password = "IamTheAdmin!"
message = username+":"+password

message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
headers = {
    'Authorization': 'Basic ' + base64_message,
    'Content-Type': 'application/json',
    'accept': 'application/json'
    }


def test_good_standardisation():
    entry_dict = {
        'age': 28,
        'balance': 6332,
        'duration': 149,
        'campaign': 1,
        'pdays': 343,
        'previous': 4
    }

    r = requests.post(url, headers=headers, json=entry_dict)
    return_dict = r.json()

    expected_dict = {
        'age': -0.65,
        'balance': 3.65,
        'duration': -0.30,
        'campaign': -0.5,
        'pdays': 15.82
    }

    assert return_dict == expected_dict


def test_second_good_standardisation():
    entry_dict = {
        'age': 41,
        'balance': -233,
        'duration': 1156,
        'campaign': 2,
        'pdays': -1,
        'previous': 0
    }

    r = requests.post(url, headers=headers, json=entry_dict)
    return_dict = r.json()

    expected_dict = {
        'age': 0.12,
        'balance': -0.49,
        'duration': 2.52,
        'campaign': 0.00,
        'pdays': 0.00
    }

    assert return_dict == expected_dict