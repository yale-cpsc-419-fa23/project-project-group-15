import argparse
import sqlite3 as sql
from contextlib import closing
import random

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



def fill_database():
    fill_colleges()
    fill_games()
    fill_players()


def fill_colleges():
    real_colleges=[
        'Benjamin Franklin',
        'Berkeley',
        'Branford',
        'Davenport',
        'Ezra Stiles',
        'Grace Hopper',
        'Jonathan Edwards',
        'Morse College',
        'Pauli Murray',
        'Pierson',
        'Saybrook',
        'Silliman',
        'Timothy Dwight',
        'Trumbull'
    ]

    fake_colleges = [
        "Fluffleworth",
        "Wobblestone",
        "Gigglington",
        "Noodlewood",
        "Tumbleton",
        "Quizzical",
        "Spindlewhack",
        "Blibberfudge",
        "Doodlefern",
        "Puffington",
        "Wibblywobble",
        "Flibberjig",
        "Snickerdoodle",
        "Whimsickle"
    ]

    ex_statement=f'''
    INSERT INTO colleges(id, name)
    VALUES 
    
    {', '.join([f'({i}, "{n}")' for i,n in enumerate(real_colleges)])};
    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)


def fill_players():
    # Posh-sounding first names
    first_names = [
        "Alistair", "Archibald", "Augustine", "Beatrice", "Benedict",
        "Bertram", "Blythe", "Caledonia", "Camilla", "Cassandra",
        "Cedric", "Charlton", "Cholmondeley", "Clarissa", "Constance",
        "Cornelius", "Cosima", "Daphne", "Deirdre", "Demetrius",
        "Dorothea", "Eleanora", "Elspeth", "Evangeline", "Fabian",
        "Felicity", "Fenwick", "Ferdinand", "Gwendoline", "Harriet",
        "Horatio", "Isadora", "Jocasta", "Julian", "Lavinia",
        "Lawrence", "Lucinda", "Magdalena", "Marmaduke", "Maximilian",
        "Meredith", "Millicent", "Montgomery", "Morwenna", "Nathaniel",
        "Octavia", "Ophelia", "Penelope", "Percival", "Persephone",
        "Phineas", "Quinton", "Rafferty", "Reginald", "Roderick",
        "Rosalind", "Rowena", "Sebastian", "Seraphina", "Sibylla",
        "Sinclair", "Sophronia", "Tamsin", "Thaddeus", "Theodora",
        "Theodore", "Tristram", "Ursula", "Valentina", "Verity",
        "Victoria", "Vivienne", "Wilfred", "Winifred", "Yvette",
        "Yolanda", "Zachariah", "Zebedee", "Agatha", "Algernon",
        "Anastasia", "Auberon", "Barnaby", "Cecily", "Cuthbert",
        "Georgiana", "Henrietta", "Ignatius", "Isolde", "Jebediah",
        "Leopold", "Marjorie", "Neville", "Orlaith", "Piers",
        "Quinlan", "Rupert", "Tallulah", "Ursuline", "Vivian"
    ]

    # Posh-sounding last names
    last_names = [
        "Abernathy", "Altringham", "Astor", "Beauchamp", "Belvoir",
        "Blackwood", "Blythwood", "Broughton", "Carrington", "Cavendish",
        "Chamberlain", "Chatsworth", "Cholmondeley", "Crichton", "Crofton",
        "Cumberland", "De Burgh", "De Vere", "Doncaster", "Dorchester",
        "Dumbleton", "Elmsworth", "Fairfax", "Featherington", "Fitzroy",
        "Fortescue", "Foxworth", "Gainsborough", "Grantham", "Grimaldi",
        "Hargreaves", "Harrington", "Haverbrook", "Haworth", "Heathcote",
        "Hightower", "Huntingdon", "Kensington", "Kingsley", "Lancaster",
        "Lavington", "Lennox", "Lockwood", "Loxley", "Lysander",
        "Mainwaring", "Mandeville", "Marchmain", "Marlborough", "Montague",
        "Moreton", "Mortimer", "Northumberland", "Oakenshield", "Ormsby",
        "Pembroke", "Pennington", "Petherington", "Ravenscroft", "Redcliffe",
        "Rockingham", "Rothschild", "Rutherford", "Saxby", "Sefton",
        "Sherborne", "Sinclair", "Somerset", "Standish", "St. Clair",
        "Strathmore", "Talbot", "Templeton", "Throckmorton", "Trelawny",
        "Trevelyan", "Upton", "Vanburgh", "Venables", "Wadsworth",
        "Walpole", "Wentworth", "Westerley", "Wetherby", "Whittington",
        "Wimborne", "Windsor", "Winthrop", "Worthington", "Wycliffe",
        "Wyndham", "Yarborough", "York", "Zouch", "Ashford",
        "Beresford", "Clifton", "Danvers", "Ellington", "Fitzwilliam"
    ]

    names=[f'{f} {l}' for f,l in zip(first_names, last_names)]

    for i,n in enumerate(names):
        id=add_players(n,  i%14)
        games=get_possible_games(id)
        for g in games:
            sign_up_player(id, g)

def fill_games():
    sports = [
        "Archery",
        "Badminton",
        "Basketball",
        "Boxing",
        "Cycling",
        "Diving",
        "Equestrian",
        "Fencing",
        "Gymnastics",
        "Judo"
    ]

    locations = [
        "Tilted Towers",
        "Pleasant Park",
        "Retail Row",
        "Lazy Lake",
        "Craggy Cliffs",
        "Steamy Stacks",
        "Holly Hedges",
        "Misty Meadows",
        "Slurpy Swamp",
        "Weeping Woods"
    ]

    times = [
        "2023-11-01 08:15:32",
        "2023-11-05 12:24:45",
        "2023-11-10 15:34:56",
        "2023-11-15 18:45:10",
        "2023-11-20 20:55:23",
        "2023-11-25 11:05:35",
        "2023-11-28 14:12:47",
        "2023-11-29 10:23:50",
        "2023-11-30 13:33:01",
        "2023-11-30 23:43:15"
    ]

    for s,l,t in zip(sports, locations, times):
        college1, college2=tuple(random.sample([i for i in range(14)], 2))
        add_game(l, s, t, college1, college2)


def add_game(location, sport, time, college1, college2):
    ex_statement = f'''
                SELECT COUNT(*) from games
                '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)
            data = cursor.fetchall()
            num_games=int(data[0][0])

    ex_statement = f'''
                INSERT INTO games(id, location, time, sport)
                VALUES 

                ({num_games}, "{location}", "{time}",  "{sport}")
                '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)

    ex_statement = f'''
    INSERT INTO colleges_games(c_id, g_id)
    VALUES 

    ({college1}, {num_games}),
    ({college2}, {num_games})
    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)



def add_players(name, college):
    ex_statement = f'''
                    SELECT COUNT(*) from players
                    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)
            data = cursor.fetchall()
            num_players = int(data[0][0])


    ex_statement = f'''
            INSERT INTO players(id, name, college)
            VALUES 

            ({num_players}, "{name}", {college});
            '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)

    return num_players



def sign_up_player(p_id, g_id):
    ex_statement = f'''
    INSERT INTO players_games(p_id, g_id)
    VALUES 

    ({p_id}, {g_id})
    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)


def get_college(p_id):
    ex_statement = f'''
        SELECT college FROM
        players

        WHERE id={p_id}
        '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)
            data = cursor.fetchall()
            return int(data[0][0])

def get_possible_games(p_id, start=None, end=None):
    ex_statement = f'''
    SELECT g_id FROM
    colleges_games
    
    WHERE c_id={get_college(p_id)}
    
    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)
            data = cursor.fetchall()
            return [int(d[0]) for d in data]



create_database()
fill_database()