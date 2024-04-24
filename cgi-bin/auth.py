import os
import sqlite3
import subprocess
import json
import base64
import cgi
from cryptography.fernet import Fernet
from enum import Enum
from http import cookies as Cookies
from typing import Optional
from typing import Union
from get_shirts import Shirt

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
def verify_input(
    form: cgi.FieldStorage, cookies: Cookies.SimpleCookie
) -> Optional[str]:
    token = cookies["token"].value
    username = form.getvalue("username")
    password = form.getvalue("password")
    shirt_id = form.getvalue("shirt_id")
    command = form.getvalue("command")

    if command is None:
        return "No command."

    if token is not "":
        if username is not None or password is not None:
            return "Token and credentials given."
        if shirt_id is None:
            return "Token given but no shirt_id to vote for"
        return None

    if not (username is not None and password is not None):
        return "Missing username or password."

    return None


def load_cookies() -> Cookies.SimpleCookie:
    cookies: Cookies.SimpleCookie = Cookies.SimpleCookie()
    cookies_string: Optional[str] = os.environ.get("HTTP_COOKIE")
    if cookies_string is not None:
        cookies.load(cookies_string)
    return cookies


def vote_for_shirt(user_id: int, shirt_id: int) -> Optional[str]:
    cursor = conn.cursor()
    try:
        cursor.executescript(
            f"""
INSERT INTO votes (vote_id, user_id, shirt_id) VALUES (NULL, {user_id}, {shirt_id})
"""
        )
    except sqlite3.Error as e:
        return str(e)
    return None


def get_user_id(username: str) -> Union[int, str]:
    user_ids = conn.execute(
        f"""
SELECT user_id FROM users WHERE user_name = {username}
"""
    ).fetchall()

    if user_ids is None:
        return f"No user_id found for username {username}"
    if len(user_ids) > 1:
        return f"Multiple user_id's found for username {username}"

    return int(user_ids[0])


conn = sqlite3.connect("db.sqlite")
input_cookies = load_cookies()
verify_input(form, input_cookies)
if type(verify_input) is str:
    print(verify_input)
    exit(400)

command = form.getvalue("command")
match command:
    case Commands.GET_TOKEN:
        credentials = Credentials(form.getvalue("username"), form.getvalue("password"))
        if check_credentials(credentials):
            cookies: Cookies.SimpleCookie = Cookies.SimpleCookie()
            cookies.load(encode_token(credentials))
            # set token
            exit()
    case Commands.VOTE:
        token = input_cookies["token"].value
        credentials = decode_token(token)
        if check_credentials(credentials):
            user_id_or_error = get_user_id(credentials.username)
            if type(user_id_or_error) is str:
                print(user_id_or_error)
                exit(422)
            shirt_id = form.getvalue("shirt_id")
            vote_for_shirt(user_id_or_error, shirt_id)
            exit(201)
        else:
            exit(403)
    case _:
        exit(400)
