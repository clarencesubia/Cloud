#!/usr/bin/env python3


import requests
import argparse
import json
import os


base_url = "https://api-mobile.zscalerbeta.net/papi/auth/v1" # Client Connector URL
parser = argparse.ArgumentParser(description="Retrieve ZPA Connected OTP")
parser.add_argument("-u", "--udid", required=True, help="Sample: udid=253B446D-D4A2-1F3E-DFAC-A51EDA415A55:705", metavar="") 
args = parser.parse_args()

udid = argparse.args


def main():
    jwt_token = token()
    get_otp(udid, jwt_token)


def token():
    api_key, secret_key = (os.environ.get("CONN_API_KEY"), os.environ.get("CONN_SC_KEY"))
    payload={
        "apiKey": api_key,
        "secretKey": secret_key
        }

    headers = {
            "Content-Type": "application/json"
            }

    response = requests.post(f"{base_url}/login", headers=headers, json=payload)
    if response.ok:
        print("Login successful!")
        jwt_token = json.loads(response.text)["jwtToken"]
        return jwt_token
    else:
        print(f"Error occured: {json.loads(response.text)['message']}")



def get_otp(udid, jwt_token):
    otp_uri = f"getOtp?udid={udid}"
    headers = {
        "auth-token": {jwt_token}
    }
    response = requests.get(f"{base_url}/{otp_uri}", headers=headers)
    if response.ok:
        print(json.loads(response.text)["otp"])
    else:
        print(f"Error occured: {json.loads(response.text)['message']}")


if __name__ == "__main__":
    main()