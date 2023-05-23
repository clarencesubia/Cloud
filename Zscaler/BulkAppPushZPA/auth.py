#!/usr/bin/python3

import requests
import os


# )y+b8&JcyIMO8b(&nD4[N:0&9QwCcpS>
# 288257933735624704

tenant = 'config.private.zscaler.com'
# customer_id = '288257933735624704'

auth_url = f"https://{tenant}/signin"

client_id, client_secret = (os.environ.get('ZPA_CL_ID'), os.environ.get('ZPA_SC'))
payload = f'client_id={client_id}&client_secret={client_secret}'
print(payload)
session = requests.Session()


headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = session.post(auth_url, headers=headers, data=payload).json()
bearerToken = response["access_token"]
access_header = {'Content-type': 'application/json', 'Authorization': f'Bearer {bearerToken}'}

print(access_header)