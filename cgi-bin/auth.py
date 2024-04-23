import os
import subprocess
import json
import base64
import cgi
from cryptography.fernet import Fernet
from enum import Enum
from http import cookies
from typing import Optional

ENCRYPTION_TOKEN = "changeMe"
fernet = Fernet(ENCRYPTION_TOKEN)
form = cgi.FieldStorage()

class Commands(Enum):
    GET_TOKEN = 0
    VOTE = 1

class Credentials:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


def check_credentials(credentials: Credentials) -> bool:
    process = subprocess.run(
        [
            r"ldapsearch",
            r"-x",
            r"-H",
            r"ldaps://ad.ucc.gu.uwa.edu.au/",
            r"-D",
            f'"cn={credentials.username},cn=Users,dc=ad,dc=ucc,dc=gu,dc=uwa,dc=edu,dc=au"',
            f"-w {credentials.password}",
            r"-b",
            r'"dc=ad,dc=ucc,dc=gu,dc=uwa,dc=edu,dc=au"',
            f'"(cn={credentials.username})"',
        ]
    )
    return process.returncode == 0


def encode_token(credentials: Credentials) -> str:
    cred_dict = {"username": credentials.username, "password": credentials.password}
    cred_json = json.dumps(cred_dict).encode("utf-8")
    cred_json_encrypted = fernet.encrypt(cred_json)

    return base64.b64encode(cred_json_encrypted).decode("ascii")


def decode_token(token: str) -> Credentials:
    encrypted_json = base64.b64decode(token.encode("ascii"))
    cred_json = fernet.decrypt(encrypted_json).decode("utf-8")
    cred_dict = json.loads(cred_json)

    return Credentials(cred_dict.get("username"), cred_dict.get("password"))

# Valid inputs:
# Token + command
# Credentials + command
# Returns an error message or `None`
def verify_input(form: cgi.FieldStorage, cookies: cookies.SimpleCookie) -> Optional[str]:
    token = cookies["token"].value
    username = form.getvalue("username")
    password = form.getvalue("password")
    command = form.getvalue("command")

    if (command is None):
        return "No command."
    
    if token is not "":
        if (username is not None or password is not None):
            return "Token and credentials given."
        return None
        
    if not (username is not None and password is not None):
        return "Missing username or password."

    return None

def load_cookies() -> cookies.SimpleCookie:
    cookies_instance: cookies.SimpleCookie = cookies.SimpleCookie()
    cookies_string: Optional[str] = os.environ.get('HTTP_COOKIE')
    if cookies_string is not None:
        cookies_instance.load(cookies_string)
    return cookies_instance

input_cookies = load_cookies()
verify_input(form, input_cookies)

command = form.getvalue("command")
match command:
    case Commands.GET_TOKEN:
        credentials = Credentials(form.getvalue("username"), form.getvalue("password"))
        if (check_credentials(credentials)):
            c: cookies.SimpleCookie = cookies.SimpleCookie()
            c.load(encode_token(credentials))
            # set token
            exit()
    case Commands.VOTE:
        token = input_cookies["token"].value
        credentials = decode_token(token)
        if (check_credentials(credentials)):
            # vote for user in credentials, exit
            exit()
    case _:
        exit()