import argparse
import sqlite3 as sql
from contextlib import closing

def create_database():
    ex_statements=[]

    ex_statements.append('''
    DROP TABLE IF EXISTS colleges;
    ''')

    ex_statements.append('''
    CREATE TABLE colleges(
    id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
    );
    ''')

    ex_statements.append('''
    DROP TABLE IF EXISTS games;
        ''')

    ex_statements.append('''
    CREATE TABLE games(
    id INT PRIMARY KEY NOT NULL,
    location TEXT,
    time TEXT,
    sport TEXT
    );
        ''')

    ex_statements.append('''
    DROP TABLE IF EXISTS colleges_games;
    ''')

    ex_statements.append('''
    CREATE TABLE colleges_games(
    c_id INT NOT NULL,
    g_id INT NOT NULL,
    winner INT DEFAULT FALSE,
    score INT,
    FOREIGN KEY(c_id) REFERENCES colleges(id),
    FOREIGN KEY(g_id) REFERENCES  games(id),
    PRIMARY KEY(c_id, g_id)
    );
        ''')

    ex_statements.append('''
    DROP TABLE IF EXISTS players;
        ''')

    ex_statements.append('''
    CREATE TABLE players(
        id INT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        college INT NOT NULL,
        FOREIGN KEY(college) REFERENCES colleges(id)
    );
        ''')

    ex_statements.append('''
    DROP TABLE IF EXISTS players_games;
            ''')

    ex_statements.append('''
    CREATE TABLE players_games(
        p_id INT NOT NULL,
        g_id INT NOT NULL,
        FOREIGN KEY(p_id) REFERENCES colleges(id),
        FOREIGN KEY(g_id) REFERENCES  games(id),
        PRIMARY KEY(p_id, g_id)
    );
            ''')



    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            for ex_statement in ex_statements:
                cursor.execute(ex_statement)


create_database()