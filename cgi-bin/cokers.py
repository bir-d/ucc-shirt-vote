import datetime
import shlex


def check_valid_date(line: str) -> bool:
    valid_date = datetime.date(2024, 2, 1)
    line_date = line[:6].split()
    return (
        valid_date
        <= datetime.datetime.strptime(
            "2024#" + line_date[0] + "#" + line_date[1].zfill(2), "%Y#%b#%d"
        ).date()
    )


with open(r"\Users\bird\Documents\cokelog", "r") as cokelog:
    dispense_lines = filter(lambda line: "merlo odispense2: dispense" in line, cokelog)
    lines_in_date = filter(check_valid_date, dispense_lines)
    lines_from_user = filter(lambda line: "bird" in line, lines_in_date)
    balances = map(lambda line: int(shlex.split(line)[13][:-1]), lines_from_user)
    print(sum(balances))
