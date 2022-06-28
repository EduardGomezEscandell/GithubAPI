#!/usr/bin/env python3
import json
from os import access
import subprocess
from personal_access_token.secret import decrypt
import time

def sanitize(argument: str) -> str:
    return argument.replace('\\', "\\\\").replace('"', '\\"')

def generate_command(command: str, args: list) -> str:
    for key, value in args:
        key   = f' {key}'               if key   else ''
        value = f' "{sanitize(value)}"' if value else ''
        command = f'{command}{key}{value}'

    return command

def stringify(data: dict) -> str:
    string = ""
    for key, value in data.items():
        string = f"{string}&{key}={value}"
    return string

with open("client_id.txt") as f:
    CLIENT_ID = f.read()

# STEP 1 - AUTHENTICATE
data = {
    "client_id": CLIENT_ID,
    "scope": "public_repo"
}

args = [
    ("-X", "POST"),
    ('-H',  'Accept: application/vnd.github.v3+json'),
    (None, "https://github.com/login/device/code"),
    ('-d', stringify(data)),
]

cmd = generate_command("curl", args)
print("----\n", cmd, "\n----\n")
result = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
response = json.loads(result)

print("Input the following code into your browser:")
print(f'URL:  {response["verification_uri"]}')
print(f'Code: {response["user_code"]}')
interval = response['interval']
maxtime = response['expires_in']

# Step 2 - Validate authentication
authentication_complete = False
start = time.time()

data = {
    "client_id": CLIENT_ID,
    "device_code": f'{response["device_code"]}',
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
}
args = [
    ("-X", "POST"),
    ('-H',  'Accept: application/vnd.github.v3+json'),
    (None, "https://github.com/login/oauth/access_token"),
    ('-d', stringify(data)),
]

while not authentication_complete:
    if time.time() - start > maxtime:
        raise RuntimeError("Failed to authenticate in time")
    time.sleep(interval + 1)

    cmd = generate_command("curl", args)
    result = subprocess.check_output(cmd, shell=False, text=True, encoding='utf-8')
    print("---")
    print(result)
    print("---")
    response = json.loads(result)
    if "error" in response:
        if response["error"] == "slow_down":
            interval = response["interval"]
    else:
        authentication_complete = True
        access_token =  response["access_token"]

# STEP 2 - ISSUE
username = "EduardGomezEscandell"

issue_data = {
    "title": "Yet another test issue",
    "body": "I opened it with github's API! Check it out, I am assigned!",
    "assignees": ["EduardGomezEscandell"],
    # "labels": ["bug", "duplicate"]
}

args = [
    # ('-i', None),
    ('-X', 'POST'),
    ('-H',  'Accept: application/vnd.github.v3+json'),
    ('-H', f"Authorization: token {access_token}"),
    (None, 'https://api.github.com/repos/EduardGomezEscandell/GithubAPI/issues'),
    ('-d', json.dumps(issue_data)),
]

cmd = generate_command("curl", args)
result = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
print(json.dumps(json.loads(result), indent=2))