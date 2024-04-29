import cgi
from http import cookies as Cookies
import os
import sys
import auth


def get_login_button() -> str:
    button = """<a href="#" class="float">"""
    button += """<h1 class="float-contents">Click here to login! </h1>"""
    button += """</a>"""
    return button


def get_login_form(error: str | None) -> str:
    form = """<a class="no-hover-float"">"""
    form += '<form class="float-contents" hx-get="/cgi-bin/action_button.py">'
    if error is not None:
        form += f"<span>{error}</span><br><br>"
    form += """
<label>username: </label><br>
<input type=text name=username></input><br>
<label>password: </label><br>
<input type=password name=password></input><br><br>
<input type="submit" value="Submit">
"""
    form += "</form>"
    form += """</a>"""
    return form


def get_vote_button() -> str:
    button = """<a class="float">"""
    button += """<h1 class="float-contents">Use </h1><h1 class="float-contents" x-text="$store.total_votes"></h1><h1 class="float-contents"> votes!</h1>"""
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
            print_http(get_vote_button())
            exit()
    else:
        username = form.getvalue("username")
        password = form.getvalue("password")
        eprint(username, password)
        if username is not None and password is not None:
            credentials = auth.Credentials(username, password)
            if auth.check_credentials(credentials):
                token_cookie: Cookies.SimpleCookie = Cookies.SimpleCookie()
                token_cookie["token"] = auth.encode_token(credentials)
                print(token_cookie.output())
                print_http(get_vote_button())
                exit()
            print_http(get_login_form("Invalid username or password."))
            exit()
        else:
            print_http(get_login_form(None))
            exit()
