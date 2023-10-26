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



def fill_database():
    fill_colleges()
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

    ex_statement = f'''
        INSERT INTO players(id, name, college)
        VALUES 

        {', '.join([f'({i}, "{n}", {i%14})' for i, n in enumerate(names)])};
        '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)



create_database()
fill_database()