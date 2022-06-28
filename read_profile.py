#!/usr/bin/env python3
import subprocess
import json
from textwrap import indent

username = "EduardGomezEscandell"

cmd = f'curl https://api.github.com/users/{username}'
result = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
print(json.dumps(json.loads(result), indent=2))