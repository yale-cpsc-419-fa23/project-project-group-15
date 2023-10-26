import argparse
import sqlite3 as sql
from contextlib import closing

def create_database():
    ex_statements=[]

    ex_statements.append('''
    DROP TABLE colleges;
    
    CREATE TABLE colleges(
    id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    
    
    );
    ''')

    ex_statements.append('''
    DROP TABLE games;
    
    CREATE TABLE games(
    id INT PRIMARY KEY NOT NULL,
    location TEXT,
    time TEXT,
    sport TEXT,
    );
    ''')




    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            pass


create_database()