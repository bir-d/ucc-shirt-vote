#!/usr/bin/python3
import cgi
from http import cookies as Cookies
import os
import sys
import auth
import cokers


def get_login_button() -> str:
    button = """<a href="#" class="float">"""
    button += """<h1 class="float-contents">Click here to login! </h1>"""
    button += """</a>"""
    return button


def get_login_form(error: str | None) -> str:
    form = """<a class="no-hover-float" style="background-color:rgb(87,255,163);" >"""
    form += '<form class="float-contents" style="background-color:rgb(87,255,163);" hx-get="/cgi-bin/action_button.py">'
    form += "<h3>You should login:</h3>"
    if error is not None:
        form += f"<span>{error}</span><br><br>"
    form += """
<label>username: </label><br>
<input type=text name=username></input><br>
<label>password: </label><br>
<input type=password name=password></input><br><br>
<input type="submit" value="Submit">
<h4></h4>
<div class="loader htmx-indicator"></div>

"""
    form += "</form>"
    form += """</a>"""
    return form


def get_vote_button(username: str, message: str | None = None) -> str:
    votes_remaining = cokers.get_votes_remaining(username)
    if votes_remaining > 0:
        button = """<a class="float" style="background-color:rgb(87, 255, 163);">"""
        button += """<div hx-post='/cgi-bin/democracy.py' hx-swap="none" hx-vals='js:{votes: Alpine.store("shirt_votes")}' class="float-contents" class="vote-button">"""
        if message is not None:
            button += f"<h2>{message}</h2><br><br>"
        button += (
            f"""<h4>Hi {username}!</h4><h4>You have {votes_remaining} votes left.</h4>"""
        )
        button += """<h1>Use </h1><h1 x-text="$store.total_votes"></h1><h1> votes!</h1>"""
        button += """<div class="loader htmx-indicator"></div>"""
        button += """</a>"""
    else:
        button = """<a class="float" style="background-color: rgb(255 87 87);">"""
        button += """<div class="float-contents">"""
        button += """<h4>You have no votes left :(</h4>"""
        button += """<h4>Spend some money in UCC to get more!</h4>"""
        button += """<h4>(Votes refresh every minute)</h4>"""
        button += """<button onClick="window.location.reload();">Refresh Page</button>"""
        button += """<h4></h4>"""
        button += """</div>"""
        button += """</a>"""
    return button


def load_cookies() -> Cookies.SimpleCookie:
    cookies: Cookies.SimpleCookie = Cookies.SimpleCookie()
    cookies_string = os.environ.get("HTTP_COOKIE")
    if cookies_string is not None:
        cookies.load(cookies_string)
    return cookies


header_printed = False


def print_http(content: str):
    if not header_printed:
        print("Content-Type: text/html")
        print()
    print(content)


# https://stackoverflow.com/a/14981125
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    form = cgi.FieldStorage()
    cookies = load_cookies()
    token = cookies.get("token")
    if token is not None:
        credentials = auth.decode_token(token.value)
        if auth.check_credentials(credentials):
            print_http(get_vote_button(credentials.username))
            exit()
    else:
        username = form.getvalue("username")
        password = form.getvalue("password")
        eprint(username, password)
        if username is not None and password is not None:
            credentials = auth.Credentials(username, password)
            if auth.check_credentials(credentials):
                auth.add_user_if_not_exists(username)
                token_cookie: Cookies.SimpleCookie = Cookies.SimpleCookie()
                token_cookie["token"] = auth.encode_token(credentials)
                print(token_cookie.output())
                print_http(get_vote_button(credentials.username))
                exit()
            print_http(get_login_form("Invalid username or password."))
            exit()
        else:
            print_http(get_login_form(None))
            exit()
