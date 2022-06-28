### Github API test

This repository exists for me to learn about Github's REST API

### How to use
First, you need to create a personal access token from github. You copy it.
Then you go run the following command:
```
python secret.py encrypt
```
and follow the instructions. This will encrypt your personal access token into a file called `encrypted_token.txt`. You only need to do this the first time.

Then, you can create issues with:
```
python new_issue.py
```
It will ask for a password in order to decrypt your personal access token. You can modify the data in `new_issue.py` in order to fit your needs.