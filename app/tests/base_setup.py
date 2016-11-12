import json
from base64 import b64encode


def post_a_bucketlist(test_client, token):
    headers = authorization_header(token)
    body = {
        "name": "Meet Nelson Mandela",
    }
    response = send_post(test_client, 'api/v1.0/bucketlists/', body, headers)
    return response


def authorization_header(token):
    headers = {
        'Authorization': 'Bearer ' + (b64encode((token + ':unused')
                                               .encode('utf-8'))
                                     .decode('utf-8'))
    }
    return headers
