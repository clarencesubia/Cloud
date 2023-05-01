#!/usr/bin/python3

import requests
import os

tenant = 'config.beta.zscalernode.com'
customer_id = '72064120240XXX'

auth_url = f"https://{tenant}/signin"

client_id, client_secret = (os.environ.get('ZPA_CL_ID'), os.environ.get('ZPA_SC'))
payload = f'client_id={client_id}&client_secret={client_secret}'

session = requests.Session()


headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = session.post(auth_url, headers=headers, data=payload).json()
bearerToken = response["access_token"]
access_header = {'Content-type': 'application/json', 'Authorization': f'Bearer {bearerToken}'}