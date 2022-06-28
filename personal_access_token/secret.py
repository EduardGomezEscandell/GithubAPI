#!/usr/bin/env python3
from getpass import getpass
import os, sys

############# Copy-pasted from https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password #############
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BACKEND = default_backend()
DEFAULT_ITERATIONS = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=BACKEND)
    return b64e(kdf.derive(password))

def _password_encrypt(message: bytes, password: str, iterations: int = DEFAULT_ITERATIONS) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def _password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

############################### End of copy-paste ########################################

class _TempFile:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __enter__(self):
        with open(self.name, "w+") as f:
            f.write(self.text)

    def __exit__(self, *_):
        os.remove(self.name)

def encrypt() -> bytes:
    tmpfilename = "secret.txt"
    with _TempFile(tmpfilename, "Remove this text and write your secret. This file will self-destruct."):
        os.system(tmpfilename)
        with open(tmpfilename, "r") as f:
            secret = "\n".join(f.readlines())
        return _password_encrypt(secret.encode('utf-8'), getpass("Input your password: "))

def decrypt(data: bytes) -> bytes:
    return _password_decrypt(data, getpass("Input your password: "))
    
def main() -> None:
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        print()
        print("Usages:")
        print()
        print("$ python secret.py help                 Shows this screen")
        print()
        print("$ python secret.py encrypt              Encrypts a message with a password.")
        print("                                        Do not write your message in the command line,")
        print("                                        you'll be prompted during execution instead.")
        print()
        print("$ python secret.py decrypt <message>    Decrypts a message with a password.")
        print()
    elif sys.argv[1] == "encrypt":
        encrypted = encrypt().decode('utf-8')
        print(encrypted)
    elif sys.argv[1] == "decrypt":
        if len(sys.argv) != 3:
            raise RuntimeError("decrypt requires the message to decrypt")
        decrypted = decrypt(sys.argv[2]).decode('utf-8')
        print(decrypted)

if __name__ == '__main__':
    main()

