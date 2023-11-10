from flask import Flask, render_template, request, jsonify, make_response, redirect, session, current_app
from werkzeug.exceptions import BadRequestKeyError
from db_creator import get_teams
from db_query import search_games
from db_creator import sign_up_player
from contextlib import closing
import secrets
from db_creator import get_players
from db_creator import test
from db_query import get_college_ranking

app = Flask(__name__, template_folder='.')
from flask_cas import CAS

CAS(app)
app.config['CAS_SERVER'] = 'https://secure.its.yale.edu'
app.config['CAS_LOGIN_ROUTE']='/cas/login'
app.config['CAS_AFTER_LOGIN'] = 'cas_testing'
app.secret_key = secrets.token_urlsafe(16)


@app.route('/')
def main_page():
    search_terms = {}

    return render_template('main.html', search_terms=search_terms)

@app.route('/games', methods=['POST', 'GET'])
def games():

    terms = {}
    try:
        terms['sport'] =request.args['sport']
    except BadRequestKeyError:
        terms['sport'] =request.cookies.get('s') or ''
    try:
        terms['college']=request.args['college']
    except BadRequestKeyError:
        terms['college']=request.cookies.get('c') or ''
    try:
        terms['start_date']=request.args['start_date']
    except BadRequestKeyError:
        terms['start_date']=request.cookies.get('sd') or ''
    try:
        terms['end_date']=request.args['end_date']
    except BadRequestKeyError:
        terms['end_date']=request.cookies.get('ed') or ''

    print(terms)

    resp = make_response(render_template('games.html', search_terms=terms))
    resp.set_cookie('s', terms['sport'])
    resp.set_cookie('c', terms['college'])
    resp.set_cookie('sd', terms['start_date'])
    resp.set_cookie('ed', terms['end_date'])

    return resp

@app.route('/get_events')
def get_events():
    #Fetch events from database
    events = []

    game = request.cookies.get('s')
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
        game_id = game[4]
        game_loc = game[0]
        game_date = game[1][:10]
        game_time = game[1][10:]
        game_sport = game[2]
        game_teams = game[3]

        events.append({
            'id': game_id,
            'title': game_sport,
            'start': game_date,
            'color': (0, 174, 255),
            'extendedProps': {
                #'description': str(game_teams) + " \n at " + str(game_loc)
                'description': str(game_teams),
                'loc': str(game_loc) + ", " + str(game_time)
            }
        })

    return jsonify(events)

#Signup Page
@app.route('/sign_up/<game_id>', methods=['POST', 'GET'])
def signup(game_id):
    players = get_teams(game_id)

    resp = make_response(render_template('sign_up.html', game_id=game_id, players=players))

    return resp

#Signup CONFIRMATION Page
@app.route('/confirm_signup/<game_id>', methods=['POST', 'GET'])
def confirm_signup(game_id):

    sign_up_player(request.form["netID"], game_id)

    print("Player " + str(request.form["netID"]) + " signed up!")
    #print(test(game_id))
    #print(get_players(game_id))

    return redirect('/games')

@app.route('/cas_testing')
def cas_testing():
    try:
        return render_template('cas_testing.html', username=session["CAS_USERNAME"])

    except KeyError:
        return render_template('cas_testing.html', username='an error occurred retrieving user data')
@app.route('/allgames', methods=['POST', 'GET'])
def allgames():

    terms = {}

    resp = make_response(render_template('games.html', search_terms=terms))

    return resp

@app.route('/rank', methods=['POST', 'GET'])
def rank():
    ranks = get_college_ranking()
    print(ranks)

    resp = make_response(render_template('rank.html',ranks=ranks))

    return resp
