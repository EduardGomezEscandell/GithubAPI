#!/usr/bin/env python3
from personal_access_token import authenticate as PAT_authenticate
from webauth import authenticate as WEBAUTH_authenticate
from common import open_issue
import sys

class AuthenticationMethod:
    @classmethod
    def authenticate(cls) -> str:
        raise NotImplementedError()

class WebAuthMethod(AuthenticationMethod):
    "Holds data about webauth device authentication. Feel free to change it."
    path_to_file = "webauth/client_id.txt"
    @classmethod
    def authenticate(cls) -> str:
        return WEBAUTH_authenticate(cls.path_to_file)

class PersonalAccessTokenMethod(AuthenticationMethod):
    "Holds data about personal access token authentication. Feel free to change it."
    path_to_file = "personal_access_token/encrypted_token.txt"
    @classmethod
    def authenticate(cls) -> str:
        return PAT_authenticate(cls.path_to_file)


def main():
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("Usage: python new_issue.py [webauth|pat] [--help] [--dry-run]")
        print(" dry-run     Executes the authentication method but does not create the issue.")
        print(" help        Prints this screen")
        print(" webauth     Runs webauth authentication. Mutually exclusive with pat.")
        print(" pat         Runs Presonal Access Token authentication. Mutually exclusive with pat.")
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv

    if "webauth" in sys.argv and "pat" in sys.argv:
        print("You can use only one authentication method at once.")
        sys.exit(1)
    if "webauth" in sys.argv:
        method = WebAuthMethod
    elif "pat" in sys.argv:
        method = PersonalAccessTokenMethod
    else:
        print("Please specify authentication method: webauth or pat")
        sys.exit(1)

    access_token = method.authenticate()
    issue_data = {
        "title": "Test issue",
        "body": "I opened it with github's API! Check it out, I am assigned and have labels!",
        "assignees": ["EduardGomezEscandell"],
        "labels": ["API"]
    }
    repository = "EduardGomezEscandell/GithubAPI"
    open_issue(issue_data, repository, access_token, dry_run)

if __name__ == '__main__':
    main()