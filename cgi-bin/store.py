import sqlite3
import get_shirts


def get_id_object(ids: list) -> str:
    obj = "Alpine.store('shirt_votes', {"
    for id in ids:
        obj += f"{id}: 0,"
    obj += "})"
    return obj


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite")
    shirts = get_shirts.get_shirts(conn.cursor())
    id_object = get_id_object([shirt.id for shirt in shirts])

    print("Content-Type: text/html")
    print()
    print(
        f"""
        document.addEventListener('alpine:init', () => {{
            {id_object}
            Alpine.store('total_votes', 0)
        }})
    """
    )
