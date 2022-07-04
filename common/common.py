import json
import requests

def sanitize(argument: str) -> str:
    return argument.replace('\\', "\\\\").replace('"', '\\"')

def stringify(data: dict) -> str:
    string = ""
    for key, value in data.items():
        string = f"{string}&{key}={value}"
    return string

def open_issue(issue_data: dict, repository: str, access_token: str, dry_run: bool = True):
    address = f'https://api.github.com/repos/{repository}/issues'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token {access_token}'
    }
    data = json.dumps(issue_data)
    if dry_run:
        headers['Authorization'] = headers['Authorization'].format(access_token="ACCES_TOKEN_GOES_HERE")
        
        print("REQUEST:")
        print("├─Headers:")
        print("|  └─",headers)
        print("└─Data:")
        print("   └─", data)
    else:
        headers['Authorization'] = headers['Authorization'].format(access_token=access_token)

        result = requests.post(address, headers=headers, data=data)
        result.raise_for_status()
        response = json.loads(result.text)

        print(json.dumps(json.loads(result), indent=2))