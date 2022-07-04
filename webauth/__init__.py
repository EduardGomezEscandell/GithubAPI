#!/usr/bin/env python3
import json
import requests
import time

from common import stringify

def authenticate(client_id_path: str) -> str:
    with open(client_id_path) as f:
        client_id = f.read()

    # STEP 1 - AUTHENTICATE
    data = {
        "client_id": client_id,
        "scope": "public_repo"
    }
    address = r"https://github.com/login/device/code"
    result = requests.post(address, headers={'Accept': 'application/vnd.github.v3+json'}, data=stringify(data))
    result.raise_for_status()
    response = json.loads(result.text)

    print("Input the following code into your browser:")
    print(f'URL:  {response["verification_uri"]}')
    print(f'Code: {response["user_code"]}')
    interval = response['interval']
    maxtime = response['expires_in']

    # Step 2 - Validate authentication
    start = time.time()

    data = {
        "client_id": client_id,
        "device_code": f'{response["device_code"]}',
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    address = r"https://github.com/login/oauth/access_token"

    while time.time() - start < maxtime:
        time.sleep(interval + 0.1)

        result = requests.post(address, headers={'Accept': 'application/vnd.github.v3+json'}, data=stringify(data))
        result.raise_for_status()
        response = json.loads(result.text)

        if "error" in response:
            # The API is requesting that we call it less frequently
            if response["error"] == "slow_down":
                interval = response["interval"]
        else:
            print("------\nAuthentication complete!\n------")
            return  response["access_token"]
    raise RuntimeError("Failed to authenticate in time")
