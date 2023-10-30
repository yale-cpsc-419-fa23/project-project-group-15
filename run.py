from flask import Flask, render_template, request, jsonify, make_response
import sqlite3
from werkzeug.exceptions import BadRequestKeyError
from db_query import search_games

app = Flask(__name__, template_folder='.')

@app.route('/')
def main_page():
    search_terms = {}

    return render_template('main.html', search_terms=search_terms)

@app.route('/games', methods=['POST', 'GET'])
def games():

    terms = {}
    terms['game'] = request.args['sport']
    terms['college'] = request.args['college']
    terms['start_date'] = request.args['start_date']
    terms['end_date'] = request.args['end_date']
    print(terms)

    resp = make_response(render_template('games.html', terms=terms))
    resp.set_cookie('g', terms['game'])
    resp.set_cookie('c', terms['college'])
    resp.set_cookie('sd', terms['start_date'])
    resp.set_cookie('ed', terms['end_date'])

    return resp

@app.route('/get_events')
def get_events():
    #Fetch events from database
    events = []

    game = request.cookies.get('g')
    college = request.cookies.get('c')
    start = request.cookies.get('sd')
    end = request.cookies.get('ed')

    event_terms = {}
    event_terms['sport'] = game
    event_terms['college'] = college
    event_terms['start_time'] = start
    event_terms['end_time'] = end

    results = search_games(event_terms)
    for game in results:
        game_loc = game[0]
        game_date = game[1][:10]
        game_sport = game[2]
        game_teams = game[3]

        events.append({
            'title': game_sport,
            'start': game_date,
            'extendedProps': {
                'description': str(game_teams) + " at " + str(game_loc)
            }
        })

    return jsonify(events)