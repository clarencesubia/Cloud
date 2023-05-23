import requests
import os

url = "https://config.private.zscaler.com/signin"

client_id, client_secret = (os.environ.get('ZPA_CL_ID'), os.environ.get('ZPA_SC'))

payload = f'client_id={client_id}&client_secret={client_secret}'

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
