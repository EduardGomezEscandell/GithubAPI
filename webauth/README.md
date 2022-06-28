## How to use
To follow these instructions you must be in the directory:
```
cd webauth
```

### Setup
First, you need to create an OAuth application. See the [documentation](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app).
Copy the `Client ID` into `webauth/client_id.txt`. You only need to do this the first time.

### Running it
Then, you can open new issues with:
```
python new_issue.py
```
It will give you a six-digit code and a URL to write it in. Afterwards, the bug will be sumbitted. You can modify the data in `new_issue.py` in order to fit your needs.