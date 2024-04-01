import sqlite3

conn = sqlite3.connect("db.sqlite")
c = conn.cursor()
c.executescript(
    """BEGIN TRANSACTION;

-- Table: shirts
CREATE TABLE IF NOT EXISTS shirts (
    shirt_id   INTEGER PRIMARY KEY,
    shirt_name TEXT,
    image      TEXT
);


-- Table: users
CREATE TABLE IF NOT EXISTS users (
    user_id   INTEGER PRIMARY KEY,
    user_name TEXT
);


-- Table: votes
CREATE TABLE IF NOT EXISTS votes (
    vote_id  INTEGER PRIMARY KEY,
    user_id  INTEGER REFERENCES users (user_id),
    shirt_id INTEGER REFERENCES shirts (shirt_id) 
);


COMMIT TRANSACTION;
"""
)

c.executescript(
    """
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (1, 'blue', 'images/blue.jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (2, 'red', 'images/red.jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (3, 'green', 'images/green.jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (4, 'yellow', 'images/yellow.jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (5, 'pink', 'images/pink.jpg');
"""
)

conn.commit()
