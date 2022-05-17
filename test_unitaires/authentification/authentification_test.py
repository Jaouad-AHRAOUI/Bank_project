import pytest
import requests
import base64
import os


# définition de l'adresse de l'API
api_address = 'localhost'
# port de l'API
api_port = 8000
# url to get the user
url='http://{address}:{port}/user'.format(address=api_address, port=api_port)

'''
1er test : administrateur avec le correct mot de passe
'''

def test_good_authent():
    # header with credentials

    username = "admin"
    password = os.environ.get("ADMIN_PASSWORD")
    message = username+":"+password

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = {'Authorization': 'Basic ' + base64_message}

    r = requests.get(url, headers=headers)

    # statut de la requête
    status_code = r.status_code

    assert status_code == 200





'''
2ème test : Audrey:SunShine123 (paire correcte)
'''

def test_second_good_authent():
    # header with credentials
    username = "audrey"
    password = "SunShine123"

    message = username+":"+password

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = {'Authorization': 'Basic ' + base64_message}

    r = requests.get(url, headers=headers)

    # statut de la requête
    status_code = r.status_code

    assert status_code == 200




'''
3ème test : jaouad:NeMarchePas (paire non existante)
'''

def test_bad_authent():
    # header with credentials
    username = "jaouad"
    password = "NeMarchePas"

    message = username+":"+password

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    headers = {'Authorization': 'Basic ' + base64_message}

    r = requests.get(url, headers=headers)

    # statut de la requête
    status_code = r.status_code
    print(status_code)

    assert status_code == 401