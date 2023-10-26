from flask import Flask, render_template, request

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

