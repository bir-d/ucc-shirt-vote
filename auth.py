import subprocess
import json
import base64
import cgi
from cryptography.fernet import Fernet
from typing import Optional

ENCRYPTION_TOKEN = "changeMe"
fernet = Fernet(ENCRYPTION_TOKEN)
form = cgi.FieldStorage()


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


# Returns an error message or `None`
def verify_input(form: cgi.FieldStorage) -> Optional[str]:
    token = form.getvalue("token")
    username = form.getvalue("username")
    password = form.getvalue("password")
    command = form.getvalue("command")

    # check input here...

    return None


verify_input(form)
