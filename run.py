from flask import Flask, render_template, request, jsonify

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
    # Fetch events from database

    #Assign to events variable like this
    events = [
        {
            'title': 'Event 1',
            'start': '2023-10-27'
        },
        {
            'title': 'Event 2',
            'start': '2023-10-28'
        }
        # Add more events as needed
    ]
    return jsonify(events)