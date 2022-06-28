#!/usr/bin/env python3
import json
from os import access
import subprocess
import time

from common import curl, stringify

def authenticate(client_id_path: str) -> str:
    with open(client_id_path) as f:
        client_id = f.read()

    # STEP 1 - AUTHENTICATE
    data = {
        "client_id": client_id,
        "scope": "public_repo"
    }

    args = [
        ("-X", "POST"),
        ('-H',  'Accept: application/vnd.github.v3+json'),
        (None, "https://github.com/login/device/code"),
        ('-d', stringify(data)),
    ]

    cmd = curl(args)
    result = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
    response = json.loads(result)

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
    args = [
        ("-X", "POST"),
        ('-H',  'Accept: application/vnd.github.v3+json'),
        (None, "https://github.com/login/oauth/access_token"),
        ('-d', stringify(data)),
    ]
    cmd = curl(args)

    while time.time() - start < maxtime:
        time.sleep(interval + 0.1)

        result = subprocess.check_output(cmd, shell=False, text=True, encoding='utf-8')
        response = json.loads(result)

        if "error" in response:
            # The API is requesting that we call it less frequently
            if response["error"] == "slow_down":
                interval = response["interval"]
        else:
            print("------\nAuthentication complete!\n------")
            return  response["access_token"]
    raise RuntimeError("Failed to authenticate in time")
