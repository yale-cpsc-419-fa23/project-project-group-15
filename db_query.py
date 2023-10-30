import argparse
import sqlite3 as sql
from contextlib import closing
import random

#sport, college, start_date, enddate

def search_games(args):
    ex_statement='''
    SELECT MIN(location), MIN(time), MIN(sport), GROUP_CONCAT()
    
    FROM
    
    
    
    '''