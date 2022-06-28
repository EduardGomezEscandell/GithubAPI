#/bin/env python3
import subprocess
import json
from textwrap import indent

cmd = 'curl https://api.github.com/users/EduardGomezEscandell'
result = subprocess.check_output(cmd, shell=True, text=True, encoding='utf-8')
print(json.dumps(json.loads(result), indent=2))