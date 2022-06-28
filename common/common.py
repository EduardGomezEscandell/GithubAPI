import json
import subprocess

def sanitize(argument: str) -> str:
    return argument.replace('\\', "\\\\").replace('"', '\\"')

def curl(args: list) -> str:
    command = "curl"
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

def open_issue(issue_data: dict, repository: str, access_token: str, dry_run: bool = True):
    args = [
        # ('-i', None),
        ('-X', 'POST'),
        ('-H',  'Accept: application/vnd.github.v3+json'),
        ('-H', f"Authorization: token {access_token}"),
        (None, f'https://api.github.com/repos/{repository}/issues'),
        ('-d', json.dumps(issue_data)),
    ]
    if dry_run:
        args = [(arg[0], arg[1].replace(access_token, "<ACCESS_TOKEN_GOES_HERE>")) for arg in args] # Anonymizing
        cmd = curl(args)
        print(cmd)
    else:
        cmd = curl(args)
        result = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
        print(json.dumps(json.loads(result), indent=2))