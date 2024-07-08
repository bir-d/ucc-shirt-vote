#!/usr/bin/python3
import cgi
import sqlite3
import sys
import get_shirts
import action_button
import auth
import cokers
import json as Json


# https://stackoverflow.com/a/14981125
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


form = cgi.FieldStorage()
json = Json.loads(form.getvalue("votes"))

conn = sqlite3.connect("db.sqlite")
shirts = get_shirts.get_shirts(conn.cursor())
cookies = action_button.load_cookies()
token = cookies.get("token")
if token is not None:
    credentials = auth.decode_token(token.value)
    if auth.check_credentials(credentials):
        total_votes = sum(json.values())
        votes_remaining = cokers.get_votes_remaining(credentials.username)
        if votes_remaining < total_votes:
            print(
                """HX-Trigger: {"reload": "You don't have enough votes. """
                + f"""You have {votes_remaining} votes, but tried to vote a total of {total_votes} times..."""
                + """ Reloading!"}"""
            )
            print("Content-Type: text/html")
            print()
            exit()

        if sum(json.values()) == 0:
            print(
                """HX-Trigger: {"reload": "You didn't vote for anything... Reloading!"}"""
            )
            print("Content-Type: text/html")
            print()
            exit()

        for shirt_id in json.keys():
            vote = int(json[shirt_id])
            shirt_id = int(shirt_id)
            if vote == 0:
                continue
            shirt = get_shirts.get_shirt(conn.cursor(), int(shirt_id))
            uid = int(auth.get_user_id(credentials.username))
            for i in range(vote):
                auth.vote_for_shirt(uid, shirt.id)
        print("""HX-Trigger: {"reload": "Vote successful. Reloading!"}""")
        print("Content-Type: text/html")
        print()
        exit()
print(
    """HX-Trigger: {"reload": "Your request is malformed. Try clearing your cache and cookies. Reloading!"}"""
)
print("Content-Type: text/html")
print()
exit()
