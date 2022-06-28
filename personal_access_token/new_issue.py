#!/usr/bin/env python3
import os
import json
import subprocess
from personal_access_token.secret import decrypt

def sanitize(argument: str) -> str:
    return argument.replace('\\', "\\\\").replace('"', '\\"')

def generate_command(command: str, args: list) -> str:
    for key, value in args:
        key   = f' {key}'               if key   else ''
        value = f' "{sanitize(value)}"' if value else ''
        command = f'{command}{key}{value}'

    return command

# Some cryptography
with open("encrypted_token.txt", "r+") as f:
    access_token = decrypt(f.read()).decode('utf-8')

# Github data
username = "EduardGomezEscandell"

issue_data = {
    "title": "Yet another test issue",
    "body": "I opened it with github's API! Check it out, I am assigned!",
    "assignees": ["EduardGomezEscandell"],
    # "labels": ["bug", "duplicate"]
}

# cURL command
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