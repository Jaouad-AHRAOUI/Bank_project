import pytest
import requests
import base64


# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000
# url to get the user
url='http://{address}:{port}/classifier/bulk'.format(address=api_address, port=api_port)


'''
1er test : l' administrateur doit pouvoir acceder à ce endpoint lui permettant d'effectuer plusieurs predictions en même temps 
'''
def test_classifier_bulk_admin():
    # header with credentials
    username = "admin"
    password = "IamTheAdmin!"
    message = username+":"+password

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = {'Authorization': 'Basic ' + base64_message}
    
    entry_list_of_dicts = [
        {
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
        },
        {
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
                           ]

    r = requests.post(url, headers=headers, json=entry_list_of_dicts)

    # statut de la requête
    status_code = r.status_code

    assert status_code == 200
    
    
    '''
2er test : Audrey (non administrateur) ne doit pas pouvoir acceder à ce endpoint lui permettant d'effectuer plusieurs predictions en même temps
'''
def test_classifier_bulk_audrey():
    # header with credentials
    username = "audrey"
    password = "SunShine123!"
    message = username+":"+password

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = {'Authorization': 'Basic ' + base64_message}
    
    entry_list_of_dicts = [
        {
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
        },
        {
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
                           ]

    r = requests.post(url, headers=headers, json=entry_list_of_dicts)

    # statut de la requête
    status_code = r.status_code

    assert status_code == 401