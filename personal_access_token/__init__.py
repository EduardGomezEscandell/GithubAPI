#!/usr/bin/env python3
import os
import json
import subprocess
from personal_access_token.secret import decrypt

def authenticate(encrypted_token_path: str) -> str:
    # Some cryptography
    with open(encrypted_token_path, "r+") as f:
        access_token = decrypt(f.read()).decode('utf-8')
    print("------\nAuthentication complete!\n------")
    return access_token
