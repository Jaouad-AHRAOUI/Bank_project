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
Test permettant de verifier que notre modèle de classification permet d'obtenir le résultat attendu 
pour un dictionnaire de variables donné
'''


def test_get_classifier():
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