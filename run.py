from flask import Flask, render_template, request, jsonify
import sqlite3

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
    return render_template('games.html', terms=terms)

@app.route('/get_events')
def get_events():
    #Fetch events from database

    connection = sqlite3.connect("intramural.sqlite")
    crsr = connection.cursor()

    query = " SELECT sport, time FROM games"

    crsr.execute(query)
    summary = crsr.fetchall()
    #print(summary)
    events = []
    for game in summary:
        game_title = game[0]
        game_date = game[1][:10]

        events.append({
            'title': game_title,
            'start': game_date
        })

    return jsonify(events)