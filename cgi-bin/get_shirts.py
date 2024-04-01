import cgi
import cgitb
import sqlite3


class Shirt:
    def __init__(self, id, name, image, votes):
        self.id = id
        self.name = name
        self.image = image
        self.votes = votes


def get_shirts(c: sqlite3.Cursor) -> list[Shirt]:
    shirts = []

    res = c.execute("SELECT * FROM shirts;").fetchall()

    for shirt in res:
        shirt_id = shirt[0]
        shirt_name = shirt[1]
        shirt_image = shirt[2]
        shirt_votes = c.execute(
            f"""
            SELECT COUNT(*)
            FROM votes
            WHERE shirt_id = {shirt_id};
            """
        ).fetchone()[0]

        shirts.append(Shirt(shirt_id, shirt_name, shirt_image, shirt_votes))

    return shirts


def get_shirt_card(shirt: Shirt) -> str:
    html = f"""
            <div class="shirt-container">
                <div class="shirt-vote-counter"><h1 class="padded-multiline"><span>0</span></h1></div>
                <div class="shirt-card">
                    <div class="shirt-image">
                        <img src="{shirt.image}" alt="$SHIRT1" />
                    </div>
                    <div class="shirt-details">
                        <h2 class="shirt-title">{shirt.name}</h2>
                        <h4 class="shirt-votes">{shirt.votes} votes</h4>
                        <button class="add-vote-btn">Add Vote</button>
                    </div>
                </div>
            </div>"""
    return html


cgitb.enable()
conn = sqlite3.connect("db.sqlite")
shirts = get_shirts(conn.cursor())

print("Content-Type: text/html")
print()
for shirt in sorted(shirts, key=lambda shirt: shirt.votes):
    print(get_shirt_card(shirt))
