import pytest
import requests
import base64

# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000
# url to get the user
url='http://{address}:{port}/classifier'.format(address=api_address, port=api_port)

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


'''
1er test : expected result = 0
'''

def test_classifier_non_adhesion():
    entry_dict = {
            "age": 28,
            "job": "services",
            "marital": "single",
            "education": "secondary",
            "default": "no",
            "balance": 6332,
            "housing": "yes",
            "loan": "no",
            "duration": 149,
            "campaign": 1,
            "pdays": 343,
            "previous": 4,
            "poutcome": "failure"
        }

    r = requests.post(url, headers=headers, json=entry_dict)
    return_dict = r.json()

    expected_dict = {
        "predicted_class": 0,
        "proba": {
            "non_adhesion_class_0": 0.62,
            "adhesion_class_1": 0.38
        }
    }

    assert return_dict == expected_dict



'''
2eme test : expected result = 1
'''

def test_classifier_adhesion():
    entry_dict = {
            "age": 41,
            "job": "retired",
            "marital": "divorced",
            "education": "primary",
            "default": "no",
            "balance": -233,
            "housing": "yes",
            "loan": "no",
            "duration": 1156,
            "campaign": 2,
            "pdays": -1,
            "previous": 0,
            "poutcome": "unknown"
        }

    r = requests.post(url, headers=headers, json=entry_dict)
    return_dict = r.json()

    expected_dict = {
        "predicted_class": 1,
        "proba": {
            "non_adhesion_class_0": 0.41,
            "adhesion_class_1": 0.59
        }
    }

    assert return_dict == expected_dict