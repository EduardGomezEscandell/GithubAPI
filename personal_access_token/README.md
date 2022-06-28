## How to use
To follow these instructions you must be in the directory:
```
cd presonal_access_token
```

### Setup
First, you need to create a personal access token from github (see the official [documentation](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)). Copy it, then you go run the following command:
```
python secret.py encrypt
```
Follow the instructions. This will encrypt your personal access token into a file called `encrypted_token.txt`. You only need to do this the first time.

### Running it
Then, you can open new issues with:
```
python new_issue.py
```
It will ask for a password in order to decrypt your personal access token. You can modify the data in `new_issue.py` in order to fit your needs.