#!/usr/bin/python3
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


def get_shirt(c: sqlite3.Cursor, id_to_search: int) -> Shirt:
    shirt = c.execute(
        "SELECT * FROM shirts WHERE shirt_id = ?;", (id_to_search,)
    ).fetchone()
    shirt_id = shirt[0]
    shirt_name = shirt[1]
    shirt_image = shirt[2]
    shirt_votes = c.execute(
        f"""
            SELECT COUNT(*)
            FROM votes
            WHERE shirt_id = {id_to_search};
            """
    ).fetchone()[0]
    return Shirt(shirt_id, shirt_name, shirt_image, shirt_votes)


def get_shirt_card(shirt: Shirt) -> str:
    html = f"""
            <div class="shirt-container">
                <div class="shirt-vote-counter"><h1 class="padded-multiline"><span>+</span><span x-text="$store.shirt_votes[{shirt.id}]"></span></h1></div>
                <div class="shirt-card">
                    <div class="shirt-image">
                        <a href="https://demuccracy.ucc.asn.au/{shirt.image}" target="_blank">
                            <img src="{shirt.image}" alt="$SHIRT1" />
                        </a>
                    </div>
                    <div class="shirt-details">
                        <h1 class="shirt-title">{shirt.name}</h2>
                        <h4 class="shirt-votes">{shirt.votes} total votes</h4>
                        <button class="add-vote-btn" @click="if ($store.shirt_votes[{shirt.id}] >= 10) {{$store.shirt_votes[{shirt.id}] -= 10; $store.total_votes -= 10}}">-10</button>
                        <button class="add-vote-btn" @click="if ($store.shirt_votes[{shirt.id}] > 0) {{$store.shirt_votes[{shirt.id}] -= 1; $store.total_votes -= 1}}">-1</button>
                        <button class="add-vote-btn" @click="$store.shirt_votes[{shirt.id}] += 1; $store.total_votes += 1">+1</button>
                        <button class="add-vote-btn" @click="$store.shirt_votes[{shirt.id}] += 10; $store.total_votes += 10">+10</button>
                        <button class="add-vote-btn" @click="$store.total_votes -= $store.shirt_votes[{shirt.id}]; $store.shirt_votes[{shirt.id}] = 0">RESET</button>
                        <button class="add-vote-btn" onclick="window.open('https://demuccracy.ucc.asn.au/{shirt.image}', '_blank'); return false;">Open image</button>
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
#    cgitb.enable()
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
    for shirt in sorted(shirts, key=lambda shirt: shirt.votes, reverse=True):
        print(get_shirt_card(shirt))

    print("</div>")
