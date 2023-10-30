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

        if where_clause:
            where_clause = where_clause[:-4]
            # where_clause = 'WHERE ' + where_clause

        return where_clause, terms

    where_clause, terms = generate_where_clause(args)
    ex_statement = f'''
    SELECT MIN(location), MIN(time), MIN(sport), GROUP_CONCAT(c_id, ', ')
    
    FROM
    
    games JOIN colleges_games on games.id = colleges_games.g_id
    
    group by games.id
    HAVING 
    {where_clause}
    '''

    with sql.connect("intramural.sqlite") as conn:
        with closing(conn.cursor()) as cursor:
            # print(ex_statement)
            cursor.execute(ex_statement, terms)
            data = cursor.fetchall()

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

if __name__=='__main__':
    args = {
        'sport': '',
        'college': 'davenport',
        'start_time': '',
        'end_time': ''
    }

    print(search_games(args))
    print(get_college_ranking())
