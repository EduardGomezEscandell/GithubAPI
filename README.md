# Github API
This repository exists for me to learn about Github's REST API

# How to use

## Operations with no authentication required
Run:
```
python read_profile.py
```
It will print the response to console. You can modify the data in `read_profile.py` in order to fit your needs.

## Operations with required authentication
You can authnticate in any two methods:
- Webauth
- Personal access token

### Personal Access Token
**Setup**

First, you need to create a personal access token from github (see the official [documentation](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)). Copy it, then you go run the following command:
```
python secret.py encrypt > presonal_access_token/encrypted_token.txt
```
Follow the instructions. This will encrypt your personal access token into a file called `encrypted_token.txt`. You only need to do this the first time.

**Running it**

Then, you can open new issues with:
```
python new_issue.py pat
```
It will ask for a password in order to decrypt your personal access token. You can modify the data in `new_issue.py` in order to fit your needs.

### Webauth
**Setup**

First, you need to create an OAuth application. See the [documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app).
Copy the `Client ID` into `webauth/client_id.txt`. You only need to do this the first time.

**Running it**

Then, you can open new issues with:
```
python new_issue.py webauth
```
It will give you a six-digit code and a URL to write it in. Afterwards, the bug will be sumbitted. You can modify the data in `new_issue.py` in order to fit your needs.