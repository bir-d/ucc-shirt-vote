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
                <div class="shirt-vote-counter"><h1 class="padded-multiline"><span>+</span><span x-text="$store.shirt_votes[{shirt.id}]"></span></h1></div>
                <div class="shirt-card">
                    <div class="shirt-image">
                        <img src="{shirt.image}" alt="$SHIRT1" />
                    </div>
                    <div class="shirt-details">
                        <h2 class="shirt-title">{shirt.name}</h2>
                        <h4 class="shirt-votes">{shirt.votes} votes</h4>
                        <button class="add-vote-btn" @click="if ($store.shirt_votes[{shirt.id}] > 0) {{$store.shirt_votes[{shirt.id}] -= 1; $store.total_votes -= 1}}">-</button>
                        <button class="add-vote-btn" @click="$store.shirt_votes[{shirt.id}] += 1; $store.total_votes += 1">+</button>
                    </div>
                </div>
            </div>"""
    return html


def get_id_object(ids: list) -> str:
    obj = "Alpine.store('shirt_votes', {"
    for id in ids:
        obj += f"{id}: 0,"
    obj += "})"
    return obj


if __name__ == "__main__":
    cgitb.enable()
    conn = sqlite3.connect("db.sqlite")
    shirts = get_shirts(conn.cursor())
    id_object = get_id_object([shirt.id for shirt in shirts])

    print("Content-Type: text/html")
    print()
    print(
        f"""
    <div class="all-shirts">
        """
    )
    for shirt in sorted(shirts, key=lambda shirt: shirt.votes):
        print(get_shirt_card(shirt))

    print("</div>")
