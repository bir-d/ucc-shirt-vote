import datetime
import shlex
import sqlite3
import auth


def check_valid_date(line: str) -> bool:
    valid_date = datetime.date(2024, 2, 1)
    line_date = line[:6].split()
    return (
        valid_date
        <= datetime.datetime.strptime(
            "2024#" + line_date[0] + "#" + line_date[1].zfill(2), "%Y#%b#%d"
        ).date()
    )


def get_potential_credits(username: str) -> int:
    with open(r"\Users\bird\Documents\cokelog", "r") as cokelog:
        dispense_lines = filter(
            lambda line: "merlo odispense2: dispense" in line, cokelog
        )
        lines_in_date = filter(check_valid_date, dispense_lines)
        lines_from_user = filter(lambda line: username in line, lines_in_date)
        balances = map(lambda line: int(shlex.split(line)[13][:-1]), lines_from_user)
        credits = sum(balances) // 100

        return credits


def get_spent_votes(user_id: int) -> int:
    conn = sqlite3.connect("db.sqlite")
    return conn.execute(
        f"""
SELECT COUNT(*) FROM votes WHERE user_id = {user_id};
"""
    ).fetchone()[0]


def get_spent_votes_un(username: str) -> int:
    id = auth.get_user_id(username)
    print(id)
    if isinstance(id, int):
        return get_spent_votes(id)
    return 99999


def get_votes_remaining(username: str) -> int:
    id = auth.get_user_id(username)
    if isinstance(id, int):
        return get_potential_credits(username) - get_spent_votes(id)
    return 0


print(get_votes_remaining("bird"))
