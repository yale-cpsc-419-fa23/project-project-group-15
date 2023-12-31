import sqlite3 as sql
from contextlib import closing
import random
from db_query import get_college, get_teams

def create_database():
    ex_statements=[]

    ex_statements.append('''
    DROP TABLE IF EXISTS colleges;
    ''')

    ex_statements.append('''
    CREATE TABLE colleges(
    id TEXT PRIMARY KEY NOT NULL
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
    c_id TEXT NOT NULL,
    g_id INT NOT NULL,
    winner INT,
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
        id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        college TEXT NOT NULL,
        FOREIGN KEY(college) REFERENCES colleges(id)
    );
        ''')

    ex_statements.append('''
    DROP TABLE IF EXISTS players_games;
            ''')

    ex_statements.append('''
    CREATE TABLE players_games(
        p_id TEXT NOT NULL,
        g_id INT NOT NULL,
        FOREIGN KEY(p_id) REFERENCES players(id),
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
    create_winners()


def fill_colleges():
    colleges=[
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

    ex_statement=f'''
    INSERT INTO colleges(id)
    VALUES 
    
    {', '.join([f'(?)' for n in colleges])};
    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, colleges)


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

    colleges = [
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

    names=[f'{f} {l}' for f,l in zip(first_names, last_names)]

    for i,n in enumerate(names):
        id=add_players(n,  colleges[i%14])
        # games=get_possible_games(id)
        # for g in games:
        #     if not sign_up_player(id, g):
        #         raise 'invalid sign up'

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

    colleges = [
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

    for l,t in zip(locations, times):
        for s in sports:
            college1, college2=tuple(random.sample(colleges, 2))
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

    args=[num_games, location, time, sport]
    ex_statement = f'''
                INSERT INTO games(id, location, time, sport)
                VALUES 

                (?, ?, ?,  ?)
                '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)

    args=college1, num_games, college2, num_games
    ex_statement = f'''
    INSERT INTO colleges_games(c_id, g_id)
    VALUES 

    (?, ?),
    (?, ?)
    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)



def add_players(name, college, id=''):
    ex_statement = f'''
                    SELECT COUNT(*) from players
                    '''

    if not id:
    # print(ex_statement)
        with sql.connect("intramural.sqlite") as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(ex_statement)
                data = cursor.fetchall()
                id = int(data[0][0])


    args=id, name, college
    ex_statement = f'''
            INSERT INTO players(id, name, college)
            VALUES 

            (?, ?, ?);
            '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)

    return id



def sign_up_player(p_id, g_id):
    player_college=get_college(p_id)
    teams=[t[0] for t in get_teams(g_id)]
    if player_college in teams:

        args=p_id, g_id
        ex_statement = f'''
        INSERT INTO players_games(p_id, g_id)
        VALUES 
        
        (?, ?)
            '''

            # print(ex_statement)

        with sql.connect("intramural.sqlite") as conn:
            with closing(conn.cursor()) as cursor:
                try:
                    cursor.execute(ex_statement, args)
                except sql.IntegrityError:
                    # print('cannot sign up player')
                    return False
        return True
    return False


def create_winners():
    ex_statement = f'''
                    SELECT COUNT(*) from games
                    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement)
            data = cursor.fetchall()
            num_games = int(data[0][0])


    for g_id in range(num_games):
        colleges=[t[0] for t in get_teams(g_id)]
        c_id=random.choice(colleges)
        set_winner(c_id, g_id)
    # args=(num_games//2,)
    # ex_statement=f'''
    # UPDATE colleges_games
    # SET winner = 1
    #
    # WHERE g_id<?
    # '''
    #
    # with sql.connect("intramural.sqlite") as conn:
    #     with closing(conn.cursor()) as cursor:
    #         # print(ex_statement)
    #         cursor.execute(ex_statement, args)
    #         data = cursor.fetchall()

def set_winner(c_id, g_id):
    args=(c_id, g_id)

    colleges = [t[0] for t in get_teams(g_id)]

    if c_id in colleges:
        ex_statement = f'''
            UPDATE colleges_games
            SET winner = (c_id=?)
    
            WHERE g_id=?
            '''

        with sql.connect("intramural.sqlite") as conn:
            with closing(conn.cursor()) as cursor:
                # print(ex_statement)
                cursor.execute(ex_statement, args)

        return True

    return False



if __name__=="__main__":
    create_database()
    fill_database()
    # print(set_winner('Davenport', 100))