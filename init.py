#!/usr/bin/python3
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

# c.executescript(
#     """
# INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'blue', 'images/blue.jpg');
# INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'red', 'images/red.jpg');
# INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'green', 'images/green.jpg');
# INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'yellow', 'images/yellow.jpg');
# INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'pink', 'images/pink.jpg');
# """
# )

c.executescript(
    """
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Ariel', 'images/Ariel.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Bryce', 'images/Bryce.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Daniel(1)', 'images/Daniel(1).jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Daniel(2)', 'images/Daniel(2).jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Diarmuid', 'images/Diarmuid.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Grace', 'images/Grace.jpg');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Jarcus', 'images/Jarcus.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Jasmine_1', 'images/Jasmine_1.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Joe', 'images/Joe.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Kirsty', 'images/Kirsty.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'LeaguePlayer', 'images/LeaguePlayer.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Please_speak_up_(Joe)', 'images/Please_speak_up_(Joe).png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Roy', 'images/Roy.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'Sev', 'images/Sev.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'coxy', 'images/coxy.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'daisy+nyxablaze', 'images/daisy+nyxablaze.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'gary', 'images/gary.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'jasmine_2', 'images/jasmine_2.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'nyxablaze', 'images/nyxablaze.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'quichelorraine', 'images/quichelorraine.png');
INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, 'tpg', 'images/tpg.png');
"""
)
conn.commit()
