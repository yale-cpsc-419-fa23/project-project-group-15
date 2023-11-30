import argparse
import sqlite3 as sql
from contextlib import closing
import random


# sport, college, start_date, enddate

def search_games(args):
    def generate_where_clause(args):
        where_clause = ''
        terms = []
        if args['sport']:
            where_clause += "UPPER(sport) LIKE '%' || UPPER(?) || '%' AND "
            terms.append(args['sport'])

        if args['college']:
            where_clause += "UPPER(c_id) LIKE '%' || UPPER(?) || '%' AND "
            terms.append(args['college'])

        if args['start_time']:
            where_clause += "time>= ? AND "
            terms.append(args['start_time'])

        if args['end_time']:
            where_clause += "time<= ? AND "
            terms.append(args['end_time'])

        if 'player_threshold' in args:
            where_clause += "(player_count IS NULL OR player_count<=?) AND "
            terms.append(args['player_threshold'])


        if where_clause:
            where_clause = where_clause[:-4]
            where_clause = 'HAVING ' + where_clause

        return where_clause, terms

    where_clause, terms = generate_where_clause(args)
    ex_statement = f'''
    SELECT MIN(location), MIN(time), MIN(sport), GROUP_CONCAT(c_id, ', '), games.id, player_count

    FROM

    games JOIN colleges_games on games.id = colleges_games.g_id
    LEFT JOIN
    (   SELECT g_id, count(p_id) as 'player_count'
        FROM
        games JOIN players_games on games.id = players_games.g_id
        GROUP BY g_id) p
    on games.id=p.g_id
    
    group by games.id
    {where_clause}
    '''
    # print(ex_statement)
    # print(terms)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            # print(ex_statement)
            cursor.execute(ex_statement, terms)
            data = cursor.fetchall()
            print(data)

    return data


def get_college_ranking():
    ex_statement='''
    SELECT c_id, COUNT(*) as 'wins'
    
    FROM
    
    colleges_games
    
    WHERE winner=TRUE
    
    GROUP BY c_id
    ORDER BY wins DESC
    
    
    '''

    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            # print(ex_statement)
            cursor.execute(ex_statement)
            data = cursor.fetchall()

    return data


def get_player_info(id):
    id = str(id)
    ex_statement = '''
            SELECT *

            FROM

            players

            WHERE id=?
            '''

    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            # print(ex_statement)
            cursor.execute(ex_statement, (id,))
            data = cursor.fetchall()
            if not data:
                return []
            return data[0]
        
def get_colleges():
    search = '''
    SELECT id
    FROM colleges
    '''
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            # print(ex_statement)
            cursor.execute(search)
            data = cursor.fetchall()

    return data

def games_low_players():
    ex_statement = '''
            SELECT games.id
            FROM games JOIN players_games
            on games.id=players_games.g_id
            GROUP BY games.id
            HAVING count(p_id) = 1
            '''

    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            # print(ex_statement)
            cursor.execute(ex_statement)
            data = cursor.fetchall()
            if not data:
                return []
            return data


def get_teams(g_id):
    args = (g_id,)
    ex_statement = f'''
        SELECT c_id, GROUP_CONCAT(players.name, ', ')
        FROM colleges_games JOIN players
        on players.college=colleges_games.c_id
        WHERE g_id=?

        GROUP BY c_id
        '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)
            data = cursor.fetchall()
            return data


def get_college(p_id):
    args = (p_id,)
    ex_statement = f'''
        SELECT college FROM
        players

        WHERE id=?
        '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)
            data = cursor.fetchall()
            if not data:
                return []
            return data[0][0]


def get_possible_games(p_id, start=None, end=None):
    args = (get_college(p_id),)
    ex_statement = f'''
    SELECT g_id FROM
    colleges_games

    WHERE c_id=?

    '''

    # print(ex_statement)
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)
            data = cursor.fetchall()
            return [int(d[0]) for d in data]



def get_players(game_id):

    args=(game_id,)
    ex_statement = f'''
    SELECT name, college FROM players_games
    JOIN players
    ON players.id=players_games.p_id
    WHERE g_id = ?
    '''
    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(ex_statement, args)
            data = cursor.fetchall()
    return data


if __name__=='__main__':
    pass
    # args = {
    #     'sport': '',
    #     'college': 'davenport',
    #     'start_time': '',
    #     'end_time': ''
    # }
    #
    # print(search_games(args))
    # print(get_college_ranking())
