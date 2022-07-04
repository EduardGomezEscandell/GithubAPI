#!/usr/bin/env python3
import json
import requests

username = "EduardGomezEscandell"

cmd = f'curl https://api.github.com/users/{username}'
result = requests.get(f'https://api.github.com/users/{username}', headers={'Accept': 'application/vnd.github.v3+json'})
result.raise_for_status()
print(json.dumps(json.loads(result.text), indent=2))