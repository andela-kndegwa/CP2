import json
from base64 import b64encode


def send_post(test_client, url, body, headers=None):
    response = test_client.post(url, data=json.dumps(body), headers=headers,
                                content_type="application/json")
    return response


def register_a_user(test_client, username):
    body = {
        "username": username,
        "password": "password",
    }
    response = send_post(test_client, 'api/v1.0/auth/register', body)
    response_json = json.loads(response.data.decode('utf-8'))
    return response_json['token']


def post_a_bucketlist(test_client, token):
    headers = authorization_header(token)
    body = {
        "name": "Meet Nelson Mandela",
    }
    response = send_post(test_client, 'api/v1.0/bucketlists/', body, headers)
    return response


def authorization_header(token):
    headers = {
        'Authorization': 'Basic ' + (b64encode((token + ':unused')
                                               .encode('utf-8'))
                                     .decode('utf-8'))
    }
    return headers
