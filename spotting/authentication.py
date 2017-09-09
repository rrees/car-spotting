import os
import logging
import json

import requests
import spotting.config as config
import spotting.headers as headers

ENV = os.environ.get('ENV', 'PROD')

def obtain_user_info(code):

    token_url ="https://{domain}/oauth/token".format(domain=config.auth0['domain'])

    payload = {
        'client_id': config.auth0['client_id'],
        'client_secret': os.environ['AUTH0_SECRET'],
        'redirect_uri': config.callback_url[ENV],
        'code': code,
        'grant_type': 'authorization_code',
    }

    #logging.info(payload)

    token_info_response = requests.post(token_url, data=json.dumps(payload), headers=headers.json)

    token_info_json = token_info_response.json()

    #logging.info(token_info_json)

    if not 'access_token' in token_info_json:
        return None

    user_url = "https://{domain}/userinfo?access_token={access_token}".format(domain=config.auth0['domain'],
        access_token=token_info_json['access_token'])

    user_info_response = requests.get(user_url)
    user_info_json = user_info_response.json()

    #logging.info(user_info_json)

    return user_info_json
